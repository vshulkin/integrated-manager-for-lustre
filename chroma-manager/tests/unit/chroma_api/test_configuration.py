from copy import deepcopy
from chroma_core.models.filesystem import ManagedFilesystem
from chroma_core.models.host import ManagedHost, VolumeNode, Volume
from chroma_core.models.target import ManagedMgs, ManagedOst, ManagedMdt
import chroma_core.lib.conf_param
from tests.unit.chroma_core.helper import JobTestCaseWithHost
from tastypie.test import ResourceTestCase
import mock


class TestConfigurationDumpLoad(JobTestCaseWithHost, ResourceTestCase):
    def __init__(self, *args, **kwargs):
        JobTestCaseWithHost.__init__(self, *args, **kwargs)
        ResourceTestCase.__init__(self, *args, **kwargs)

    def setUp(self):
        JobTestCaseWithHost.setUp(self)
        ResourceTestCase.setUp(self)

        from chroma_api.authentication import CsrfAuthentication
        self.old_is_authenticated = CsrfAuthentication.is_authenticated
        CsrfAuthentication.is_authenticated = mock.Mock(return_value = True)
        self.api_client.client.login(username = 'debug', password = 'chr0m4_d3bug')
        #super(TestConfigurationDumpLoad, self).setUp()
        #self.api = tastypie_test.TestApiClient()
        self.create_simple_filesystem()

    def tearDown(self):
        from chroma_api.authentication import CsrfAuthentication
        CsrfAuthentication.is_authenticated = self.old_is_authenticated

        ResourceTestCase.tearDown(self)
        JobTestCaseWithHost.tearDown(self)

    def test_dump(self):
        response = self.api_client.get("/api/configuration/")
        self.assertHttpOK(response)
        data = self.deserialize(response)

        mgt = data['mgts'][0]
        filesystem = mgt['filesystems'][0]
        ost = filesystem['osts'][0]
        mdts = filesystem['mdts']

        self.assertEqual(filesystem['name'], self.fs.name)
        self.assertEqual(ost['name'], self.ost.name)
        self.assertEqual(mdts[0]['name'], self.mdt.name)

        return data

    def test_load(self):
        """

        """
        new_conf_params = {'llite.max_cached_mb': '16'}
        response = self.api_client.put("/api/filesystem/%s/" % self.fs.id, data = {'conf_params': new_conf_params})
        self.assertHttpAccepted(response)

        data = self.test_dump()

        # Remember where the volumes were at so we can recreate the same host
        volume_paths = [vn.path for vn in VolumeNode.objects.all()]

        # Force remove our host to tear everything down
        from chroma_core.tasks import command_run_jobs
        command_run_jobs.delay([{'class_name': 'ForceRemoveHostJob', 'args': {'host_id': self.host.id}}], "Test host force remove")

        with self.assertRaises(ManagedMgs.DoesNotExist):
            ManagedMgs.objects.get()

        # Add the host back and try re-instantiating the filesystem
        self.host, command = ManagedHost.create_from_string('myaddress')
        for path in volume_paths:
            VolumeNode.objects.create(volume = Volume.objects.create(), path = path, host = self.host, primary = True)

        response = self.api_client.post("/api/configuration/", data = data)
        self.assertHttpCreated(response)

        self.assertEqual(ManagedMgs.objects.count(), 1)
        self.assertEqual(ManagedMdt.objects.count(), 1)
        self.assertEqual(ManagedOst.objects.count(), 1)
        self.assertEqual(ManagedFilesystem.objects.count(), 1)

        fs_params = chroma_core.lib.conf_param.get_conf_params(ManagedFilesystem.objects.get())
        self.assertDictContainsSubset({'llite.max_cached_mb': '16'}, fs_params)

        self.set_state(ManagedFilesystem.objects.get(), 'available')

        # Add a hypothetical extra OST
        ost_data = deepcopy(data['mgts'][0]['filesystems'][0]['osts'][0])
        ost_data['name'] = 'foofs-OST0002'
        new_volume = self._test_lun(self.host)
        ost_data['mounts'][0]['path'] = new_volume.volumenode_set.get().path
        data['mgts'][0]['filesystems'][0]['osts'].append(ost_data)

        response = self.api_client.post("/api/configuration/", data = data)
        self.assertHttpCreated(response)

        self.assertEqual(ManagedMgs.objects.count(), 1)
        self.assertEqual(ManagedMdt.objects.count(), 1)
        self.assertEqual(ManagedOst.objects.count(), 2)
        self.assertEqual(ManagedFilesystem.objects.count(), 1)
