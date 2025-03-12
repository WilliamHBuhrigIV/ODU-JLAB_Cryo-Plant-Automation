use data_structures::{*, file_csv::CSV as CSV};
mod data_structures;
fn main() {
    let test_csv = CSV::new("./src/test.csv");
    let data: PointCloud<PointVector<DataPoint>> = CSV::load_self(&test_csv).unwrap();
    println!("{:#?}",data);
}