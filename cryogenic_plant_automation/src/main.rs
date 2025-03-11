mod data_loader;
fn main() {
    let data: Vec<Vec<f64>> = data_loader::load_csv_data("./src/test.csv");
    println!("{:#?}",data);
}