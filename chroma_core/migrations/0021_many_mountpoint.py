# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-07-02 21:27
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models

existing_mounts = {}


def gather_existing_mounts(apps, schema_editor):
    LustreClientMount = apps.get_model("chroma_core", "LustreClientMount")

    for m in LustreClientMount.objects.filter(mountpoint__isnull=False, not_deleted=True):
        existing_mounts[m.id] = m.mountpoint


def gather_existing_mounts_reverse(apps, schema_editor):
    LustreClientMount = apps.get_model("chroma_core", "LustreClientMount")

    ms = [m for m in LustreClientMount.objects.filter(not_deleted=True) if len(m.mountpoints)]

    for m in ms:
        existing_mounts[m.id] = m.mountpoints[0]


def apply_existing_mounts(apps, schema_editor):
    LustreClientMount = apps.get_model("chroma_core", "LustreClientMount")

    for m in LustreClientMount.objects.filter(id__in=existing_mounts.keys()):
        m.mountpoints.append(existing_mounts[m.id])
        m.save()


def apply_existing_mounts_reverse(apps, schema_editor):
    LustreClientMount = apps.get_model("chroma_core", "LustreClientMount")

    for m in LustreClientMount.objects.filter(id__in=existing_mounts.keys()):
        m.mountpoint = existing_mounts[m.id]
        m.save()


class Migration(migrations.Migration):

    dependencies = [
        ("chroma_core", "0020_clientmounts_remove_fk"),
    ]

    operations = [
        migrations.RunPython(gather_existing_mounts, apply_existing_mounts_reverse),
        migrations.RemoveField(model_name="lustreclientmount", name="mountpoint",),
        migrations.AddField(
            model_name="lustreclientmount",
            name="mountpoints",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.TextField(), default=list, help_text=b"Filesystem mountpoints on host", size=None
            ),
        ),
        migrations.RunPython(apply_existing_mounts, gather_existing_mounts_reverse),
    ]