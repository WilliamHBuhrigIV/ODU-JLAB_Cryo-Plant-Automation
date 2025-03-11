mod data_loader;
use data_loader::CSV as CSV;
fn main() {
    let test_csv = CSV::new("./src/test.csv");
    let data: Vec<Vec<f64>> = test_csv.load_csv_data();
    println!("{:#?}",data);
}