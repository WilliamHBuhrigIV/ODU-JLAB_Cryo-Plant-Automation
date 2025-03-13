#[allow(unused_imports)]
use {
    core::fmt, 
    super::super::data_structures::{PointData, PointVector, PointCloud},
    linear::*
};

pub mod linear;

#[derive(Debug)]
#[allow(dead_code)]
pub enum ComplexityKind {
    Linear(Linear)
}

#[derive(Debug)]
#[allow(dead_code)]
pub enum GaussianParams {
    None
}

#[derive(Debug)]
#[allow(dead_code)]
pub struct Gaussian {
    complexity: ComplexityKind,
    gaussian_params: Option<Vec<GaussianParams>>
}

impl Gaussian {
    #[inline]
    pub const fn new(complexity: ComplexityKind, gaussian_params: Option<Vec<GaussianParams>>) -> Self { Self { complexity, gaussian_params }}
}