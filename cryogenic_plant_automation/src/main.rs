use {
    data_structures::{file_csv::*, interface_sqlite::*, *}, modeling::{gaussian::{linear::*, *}, *}
};
mod data_structures;
mod modeling;

#[async_std::main]
async fn main() {
    sqlite_main_twostreamhx().await;

    // Effectivily Isn't Doing Anything Past Here 
    // Prevents Warnings from happening if being used.
    let test_csv = CSV::new("./data/test.csv");
    let mut data: PointCloud = CSV::load_self(&test_csv).unwrap();
    let x1: PointVector = data.pop().unwrap();
    let y1: PointVector = data.pop().unwrap();
    let _t1: PointVector = data.pop().unwrap();
    let mut input_cloud: PointCloud = PointCloud::new();
    input_cloud.push(x1);
    input_cloud.push(y1);
    // println!("\nInput Data:    {:?}",&input_cloud);
    let plant_params: Vec<GlobalParams>= vec![GlobalParams::None];
    let gaussian_params: Vec<GaussianParams> = vec![GaussianParams::None];
    let linear_params: Vec<LinearParams> = vec![LinearParams::None];
    let linear_gaussian_plant = 
        Plant::new(ModelKind::Gaussian(
            Gaussian::new(ComplexityKind::Linear(
                Linear::new(linear_params)),gaussian_params)),plant_params);
    let _output_cloud: PointCloud = linear_gaussian_plant.compute(input_cloud);
    // println!("\n{:?}",&linear_gaussian_plant);
    // println!("\nOutput Data:   {:?}\n",&output_cloud);
}