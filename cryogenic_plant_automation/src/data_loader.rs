use std::io::ErrorKind;
use std::io::BufReader;
use std::io::prelude::*;
use std::str;
use std::fs::File;
pub struct CSV {
    file_path: &'static str,
}
// Assumes Standard RFC 4180
// Removes Header Data
impl CSV {
    pub fn new(file_path: &'static str) -> Self { Self { file_path }}
    pub fn load_csv_data(&self) -> Vec<Vec<f64>> {
        let file = match File::open(self.file_path) {
            Ok(file) => file,
            Err(e) => match e.kind() {
                ErrorKind::NotFound => { panic!("Can't Find File: {e:?}") },
                e => { panic!("Can't Open File: {e:?}") }
            }
        };
        let mut buffer_data = BufReader::new(file);
        let mut data = String::new();
        match buffer_data.read_to_string(&mut data) {
            Ok(value) => value,
            Err(e) => match e.kind() {
                e => { panic!("Failed to Write Buffer Data: {e:?}") }
            }
        };
        let data: Vec<u8> = data.as_bytes().to_vec();
        let mut column_number: usize = 1;
        for &item in data.iter() {
            match item {
                b',' => column_number += 1,
                b'\r' => break,
                _ => continue
            }
        }
        let mut buffer_data: Vec<&str> = Vec::new();
        let mut cell_start: usize = 0;
        for (i, &item) in data.iter().enumerate() {
            if (i == data.len() - 1) && (data[i-1] != b'\r') {
                buffer_data.push(str::from_utf8(&data[cell_start..]).unwrap());
                break;
            }
            if (b',' == item) || (b'\r' == item) {
                buffer_data.push(str::from_utf8(&data[cell_start..i]).unwrap());
                cell_start = i + 1;
                if item == b'\r' {
                    cell_start += 1;
                }
            }
        }
        let mut data: Vec<Vec<f64>> = Vec::new();
        for _i in 0..column_number {
            data.push(Vec::new());
        }
        let mut line_one_header = false;
        for &item in buffer_data[..column_number].iter() { match item.parse::<f64>() {
            Ok(_) => continue,
            Err(_) => {
                line_one_header = true;
                break;
            }
        }}
        for (i, &item) in buffer_data.iter().enumerate() {
            if line_one_header && (i < column_number) {
                continue;
            }
            match i % column_number {
                value => data[value].push(match item.parse::<f64>() {
                    Ok(value) => value,
                    Err(e) => {
                        if i < column_number { continue }
                        panic!("Non Float in Data: {e:?}\nLine: {} Column: {}",i/column_number, i%column_number)
                    }
                })
            }
        }
        data
    }
}