use crate::data_structures::PointCloud;

#[derive(Debug)]
pub enum LinearParams {
    None
}

#[derive(Debug)]
pub struct Linear {
    #[allow(dead_code)]
    local_params: Vec<LinearParams>,
}

impl Linear {
    #[inline]
    pub const fn new(local_params: Vec<LinearParams>) -> Self { Self { local_params }}
    #[inline]
    pub fn compute(&self, input_data: PointCloud) -> PointCloud {
        let dat = input_data.clone();
        dat
    }
}