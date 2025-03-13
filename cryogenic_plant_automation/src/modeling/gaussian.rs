use linear::*;
use crate::data_structures::PointCloud;

pub mod linear;

#[derive(Debug)]
pub enum ComplexityKind {
    Linear(Linear)
}

#[derive(Debug)]
pub enum GaussianParams {
    None
}

#[derive(Debug)]
pub struct Gaussian {
    complexity: ComplexityKind,
    #[allow(dead_code)]
    gaussian_params: Vec<GaussianParams>
}

impl Gaussian {
    #[inline]
    pub const fn new(complexity: ComplexityKind, gaussian_params: Vec<GaussianParams>) -> Self { Self { complexity, gaussian_params }}
    #[inline]
    pub fn compute(&self, input_data: PointCloud) -> PointCloud { match &self.complexity {
        ComplexityKind::Linear(linear) => linear.compute(input_data),
        #[allow(unreachable_patterns)]
        e => panic!("Didn't Implement in Gaussian Compute: {:?}",e)
    }}
}