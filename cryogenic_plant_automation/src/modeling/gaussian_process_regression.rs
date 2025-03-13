#[allow(unused_imports)]
use super::super::data_structures::{PointData, PointVector, PointCloud};
#[allow(dead_code)]
pub struct GaussianProcessRegression {
    values: Option<ModelPrams>
}
#[allow(dead_code)]
struct ModelPrams {
    input: PointCloud<PointVector<PointData>>
}
impl GaussianProcessRegression {
    #[inline]
    pub const fn new() -> Self { Self { values: None }}
}