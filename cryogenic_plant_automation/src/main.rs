use {
    data_structures::{file_csv::*, *},
    modeling::{gaussian::{linear::*, *}, *}
};

mod data_structures;
mod modeling;

fn main() {
    let test_csv = CSV::new("./src/test.csv");
    let mut data: PointCloud = CSV::load_self(&test_csv).unwrap();
    let x1: PointVector = data.pop().unwrap();
    let y1: PointVector = data.pop().unwrap();
    let _t1: PointVector = data.pop().unwrap();
    let mut input_cloud: PointCloud = PointCloud::new();
    input_cloud.push(x1);
    input_cloud.push(y1);
    println!("\nInput Data:    {:?}",&input_cloud);
    let plant_params: Vec<GlobalParams>= vec![GlobalParams::None];
    let gaussian_params: Vec<GaussianParams> = vec![GaussianParams::None];
    let linear_params: Vec<LinearParams> = vec![LinearParams::None];
    let linear_gaussian_plant = 
        Plant::new(ModelKind::Gaussian(
            Gaussian::new(ComplexityKind::Linear(
                Linear::new(linear_params)),gaussian_params)),plant_params);
    let output_cloud: PointCloud = linear_gaussian_plant.compute(input_cloud);
    println!("\n{:?}",&linear_gaussian_plant);
    println!("\nOutput Data:   {:?}\n",&output_cloud);
}