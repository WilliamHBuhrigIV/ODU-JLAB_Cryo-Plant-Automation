use super::{common_enums::*, interface_sqlite::interface_SQLite};

////////////////////////////////////////////////////////////////////////////////
// Heatexchanger Struct Declarations
////////////////////////////////////////////////////////////////////////////////

pub struct Streams {
    time: Time,
    streams: Vec<Stream>
}

pub struct Stream {
    pressure: Pressure,
    massflow: Massflow,
    temperature_input: Temperature,
    temperature_output: Temperature
}

#[allow(dead_code)]
pub struct HeatExchanger {
    name: String,
    stream_number: u64,
    data_interface: Option<interface_SQLite>
}

////////////////////////////////////////////////////////////////////////////////
// Inherent methods for Heatexchanger
////////////////////////////////////////////////////////////////////////////////

impl Streams {
    pub fn new(time: Time, streams: Vec<Stream>) -> Self { Streams {
        time,
        streams
    }}
}

impl Stream {
    pub fn new(pressure: Pressure, massflow: Massflow, temperature_input: Temperature, temperature_output: Temperature) -> Self { Stream {
        pressure,
        massflow,
        temperature_input,
        temperature_output
    }}
}

impl HeatExchanger {
    pub async fn new(stream_number: u64,name: String) -> Self { Self {
        name: name.clone(),
        stream_number,
        data_interface: None
    }}
    pub async fn close(&self) -> () {
        match &self.data_interface {
            Some(v) => v.close().await,
            None => panic!("Tried Closing a Non-exsistant Interface")
        };
    }
    pub async fn open_new(&mut self) -> () {
        let db_uri = String::from("sqlite://data/components/heat_exchanger/") + &self.name.as_str() + ".db";
        self.data_interface = Some(interface_SQLite::new(db_uri, Component::HeatExchanger(self)).await);
    }
    pub fn create_schema_heat_exchanger(&self) -> String {
        // Creating a Header to the db File
        let mut qry = String::from(
        "PRAGMA foreign_keys = ON;
        CREATE TABLE IF NOT EXISTS component (
            component_name TEXT PRIMARY KEY NOT NULL,
            component_type TEXT NOT NULL,
            input_output_number BLOB NOT NULL,
            processed_number BLOB DEFAULT 0,
            update_on DATETIME DEFAULT (datetime('now','localtime'))
        );");
    
        // Makes the Data Table specifically for the Component
        qry.push_str("
        CREATE TABLE IF NOT EXISTS data (
            data_id INTEGER PRIMARY KEY AUTOINCREMENT,
            time DATETIME NOT NULL,
            pressure_stream_1 BLOB NOT NULL, --Pa--
            pressure_stream_2 BLOB NOT NULL, --Pa--
            massflow_stream_1 BLOB NOT NULL, --g/s--
            massflow_stream_2 BLOB NOT NULL, --g/s--
            temperature_stream_1_inlet BLOB NOT NULL, --K--
            temperature_stream_1_outlet BLOB NOT NULL, --K--
            temperature_stream_2_inlet BLOB NOT NULL, --K--
            temperature_stream_2_outlet BLOB NOT NULL --K--
        );");
    
        // Still deciding whether this should exsist here
        // qry.insert_str(qry.len(),"
        // CREATE TABLE IF NOT EXISTS process (
        //     process_id INTEGER PRIMARY KEY AUTOINCREMENT,
        //     a INTEGER NOT NULL
        // );");
    
        // TEMP creates Hx called test
        qry.push_str("
        INSERT INTO component (
            component_name, 
            component_type, 
            input_output_number, 
            processed_number
        ) Values(
            'test',
            'HeatExchanger',
            '8',
            '0' 
        );");
        return qry;
    }
    pub async fn add_data(&self, streams: Streams) -> () {
        if streams.streams.len() < self.stream_number.try_into().unwrap() {
            panic!("Stream Number Too High or Not Enough Data Point Streams Provided!");
        }
        let mut add_data_query = String::from("
            UPDATE component SET update_on = datetime('now');
            INSERT INTO data (
                time,
                pressure_stream_1,
                massflow_stream_1,
                temperature_stream_1_inlet,
                temperature_stream_1_outlet,
                pressure_stream_2,
                massflow_stream_2,
                temperature_stream_2_inlet,
                temperature_stream_2_outlet
            ) Values(");
        add_data_query += format!("
                datetime('{}')",
                streams.time,
            ).as_str();
        for (_, stream_item) in streams.streams.iter().enumerate() {
            add_data_query += format!(",
                '{}',
                '{}',
                '{}',
                '{}'",
                stream_item.massflow,
                stream_item.pressure,
                stream_item.temperature_input,
                stream_item.temperature_output
            ).as_str();
        }
        add_data_query += "
            );";
        println!("{}", &add_data_query.as_str());
        match match &self.data_interface {
            Some(v) => v,
            None => panic!("Attempted to Write data while not open")
        }.query(add_data_query).await {
            Ok(v) => println!("{:?}",v),
            Err(e) => panic!("{:?}",e)
        };
    }
}

