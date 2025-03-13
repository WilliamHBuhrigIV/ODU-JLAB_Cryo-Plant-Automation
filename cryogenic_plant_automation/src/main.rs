
#[allow(unused_imports)]
use {
    core::option::Option::{self, Some},
    data_structures::{*, file_csv::*},
    modeling::{*,gaussian::{*, linear::*}}
};

mod data_structures;
mod modeling;

fn main() {
    let test_csv = CSV::new("./src/test.csv");
    let mut data: PointCloud<PointVector<PointData>> = CSV::load_self(&test_csv).unwrap();
    let x1 = data.pop().unwrap();
    let y1 = data.pop().unwrap();
    let _t1 = data.pop().unwrap();
    let mut testing_data: PointCloud<PointVector<PointData>> = PointCloud::new();
    testing_data.push(x1);
    testing_data.push(y1);
    let plant_params= Some(vec![GlobalParams::None]);
    let gaussian_params = Some(vec![GaussianParams::None]);
    let linear_params = Some(vec![LocalParams::None]);
    let linear_gaussian_plant = 
        Plant::new(ModelKind::Gaussian(
            Gaussian::new(ComplexityKind::Linear(
                Linear::new(linear_params)),gaussian_params)),plant_params);
    println!("{:?}",linear_gaussian_plant)
}