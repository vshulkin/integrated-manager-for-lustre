use crate::generated::css_classes::C;
use seed::{prelude::*, *};

pub fn logo<T>() -> Node<T> {
    svg![
        class![C.fill_current],
        attrs! {
            At::ViewBox => "0 0 335.77 299.14",
        },
        path![
            attrs! { At::D => "M184,25.14c2.54,16.11,22.53,31.32,13,56-2.56,1.48-3.15,2.4-7,3-1.36-1.26-1.77-1.37-4-2-6.35-22.69-10.52-44.68-28-56-27.6-17.87-73.46.61-80,25,19.84,1,27.55,14.55,38,25,18.55,18.55,40.14,34.84,56,56l15,14c6.31,8.43,10,22.79,3,34-4.18,6.65-33.83,18.8-47,16-5.81-1.24-26-9-26-9-2.62,4.1-4,13.52-5,18-4.57,1.22-7.7,2.07-13,1l-1-3c-5.52-7.71,5.49-12.11,3-22-4.06-16.11-22.4-24.7-23-41,2.43-1.53,4.86-5.51,9-5,5.84.71,11.38,9.38,15,13,10.53,10.53,22.39,25.08,38,30,8.69,2.74,34.49-4.58,37-10v-7c-13.82-10.62-26.06-28.69-39-41-18-17.14-37.87-33-55-51-14.2.39-15.43,10.45-29,8-1-4-2-7-2-13,5.49-7.82,6.84-18.13,12-26,12.26-18.71,45.37-45.06,82-35,9.05,2.49,16.71,9,26,10,14-13.38,53.26-17.42,75-8,33.49,14.52,48.41,39.69,48,89,14.89,4.64,33.8,29.18,39,44,3.19,9.09,1.58,37.66-1,46-6.57,21.27-22.49,37.66-42,46-8.7,3.72-55.05,12.78-60,1-1.05-1.55-1-4.09-1-7,4.93-3.27,8.65-4.18,18-4,5.93-3.48,18,0,25-2a110.2,110.2,0,0,0,25-11c12.15-7.25,26.16-40.39,19-64-2.14-7.06-8.05-12.7-12-18-4.36-5.84-8.78-13.19-18-14-6.77,11.6-25.37,31.92-43,32-2.72-4-4.83-3.89-5-11,14.48-9.26,33.39-23.18,39-41v-14c0-32.21-21.78-51-46-59C213,11.82,196.87,22.86,184,25.14Zm-150,132c5.47,0,8.49,1,10,5,.8,1.18.77,1.68,1,4-8.87,9.33-24.11,33.77-38,36-2.44-2.52-4.66-3.16-6-7-.75-1.07-.6-.95-1-3,1.79-2.1,2.31-4.72,4-7C11.93,174.41,24.69,166.66,34,157.14Zm34,70h4c1.94,2.83,5.64,6.61,4,10-1.47,7.62-28.59,31.76-38,32-2.56-3.3-3.88-2.59-4-9,6.11-5.82,10.43-14.78,17-20C56.52,235.75,62.93,232,68,227.14Zm120,1h7c2.64,3.93,4.05,4.61,4,12l-43,43c-5.81,5.81-10.64,15-21,16-2.2-2.09-3.69-1.72-5-5-1-1.42-1-3.27-1-6a245.4,245.4,0,0,0,27-30Z", },
        ],
    ]
}