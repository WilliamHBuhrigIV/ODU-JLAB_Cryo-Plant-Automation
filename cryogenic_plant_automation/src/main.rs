use data_structures::{*, file_csv::CSV as CSV};
mod data_structures;
use modeling::{*,gaussian_process_regression::*};
mod modeling;
fn main() {
    let test_csv = CSV::new("./src/test.csv");
    let mut data: PointCloud<PointVector<PointData>> = CSV::load_self(&test_csv).unwrap();
    let vec_data = data.pop().unwrap();
    let _model = Plant::new(ModelKind::GPR(GaussianProcessRegression::new()),vec_data);
}