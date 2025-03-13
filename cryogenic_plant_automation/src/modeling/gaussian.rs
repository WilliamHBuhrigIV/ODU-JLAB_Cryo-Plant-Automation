use linear::*;
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
    gaussian_params: Option<Vec<GaussianParams>>
}

impl Gaussian {
    #[inline]
    pub const fn new(complexity: ComplexityKind, gaussian_params: Option<Vec<GaussianParams>>) -> Self { Self { complexity, gaussian_params }}
    #[inline]
    pub fn compute(&self) { match &self.complexity {
        ComplexityKind::Linear(l) => l.compute(),
        #[allow(unreachable_patterns)]
        e => panic!("Didn't Implement in Gaussian Compute: {:?}",e)
    }}
}