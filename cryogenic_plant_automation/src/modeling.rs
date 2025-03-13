#[allow(unused_imports)]
use super::data_structures::{PointData, PointVector, PointCloud};
use gaussian_process_regression::GaussianProcessRegression;
pub mod gaussian_process_regression;
#[allow(dead_code)]
pub enum ModelKind {
    GPR(GaussianProcessRegression)
}
#[allow(dead_code)]
pub struct Plant {
    model: ModelKind,
    test_data: PointVector<PointData>
}
impl Plant {
    #[inline]
    pub const fn new(model: ModelKind, test_data: PointVector<PointData>) -> Self { Self {
        model,
        test_data
    }}
}