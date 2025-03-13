use gaussian::*;

use crate::data_structures::PointCloud;
pub mod gaussian;

#[derive(Debug)]
pub enum ModelKind {
    Gaussian(Gaussian)
}

#[derive(Debug)]
pub enum GlobalParams {
    None
}

#[derive(Debug)]
pub struct Plant {
    model: ModelKind,
    #[allow(dead_code)]
    global_params: Vec<GlobalParams>
}

impl Plant {
    #[inline]
    pub const fn new(model: ModelKind, global_params: Vec<GlobalParams>) -> Self { Self { model, global_params }}
    #[inline]
    pub fn compute(&self, input_data: PointCloud) -> PointCloud { match &self.model {
        ModelKind::Gaussian(g) => g.compute(input_data),
        #[allow(unreachable_patterns)]
        e => panic!("Didn't Implement in Plant Compute: {:?}",e)
    }}
}