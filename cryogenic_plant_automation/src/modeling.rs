#[allow(unused_imports)]
use {
    std::collections::HashMap, 
    core::{fmt, write}, 
    gaussian::*, 
    super::data_structures::{PointData, PointVector, PointCloud}
};

pub mod gaussian;

#[derive(Debug)]
#[allow(dead_code)]
pub enum ModelKind {
    Gaussian(Gaussian)
}

#[derive(Debug)]
#[allow(dead_code)]
pub enum GlobalParams {
    None
}

#[derive(Debug)]
#[allow(dead_code)]
pub struct Plant {
    model: ModelKind,
    global_params: Option<Vec<GlobalParams>>
}

impl Plant {
    #[inline]
    pub const fn new(model: ModelKind, global_params: Option<Vec<GlobalParams>>) -> Self { Self { model, global_params }}
}