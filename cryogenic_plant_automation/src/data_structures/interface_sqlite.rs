use sqlx::{migrate::MigrateDatabase, sqlite::SqliteQueryResult, Pool, Sqlite, SqlitePool};

use super::{common_enums::*, file_csv::CSV, heat_exchanger::*};

#[allow(dead_code)]
#[allow(non_camel_case_types)]
pub struct interface_SQLite {
    db_uri: String,
    pool: Pool<Sqlite>
}

#[allow(dead_code)]
impl interface_SQLite {
    pub async fn new(db_uri: String, component_type: Component<'_>) -> Self { Self {
        db_uri: db_uri.clone(),
        pool: {
            if !Sqlite::database_exists(db_uri.as_str()).await.unwrap_or(false) {
                Sqlite::create_database(db_uri.as_str()).await.unwrap();
                match Self::apply_schema(&db_uri, component_type).await{
                    Ok(_) => (),
                    Err(e) => panic!("{:?}",e)
                }
            }
            SqlitePool::connect(db_uri.as_str()).await.unwrap()
        }
    }}
    // Panic if Database doesn't exists
    pub async fn open(db_uri: String) -> Self { Self {
        db_uri: db_uri.clone(),
        pool: {
            match Sqlite::database_exists(db_uri.as_str()).await {
                Ok(true) => match SqlitePool::connect(db_uri.as_str()).await {
                    Ok(v) => v,
                    Err(e) => panic!("{:?}",e)
                },
                Ok(false) => panic!("Panic!!: Database URI doesn't point to an exsisting file"),
                Err(e) => panic!("{:?}",e)
            }
        }
    }}
    pub async fn close(&self) -> () {
        self.pool.close().await;
    }
    pub async fn apply_schema(db_url: &String, component_type: Component<'_>) -> Result<SqliteQueryResult, sqlx::Error>{
        let temp_pool = SqlitePool::connect(&db_url.to_string()).await?;
        let qry: String = match component_type {
            Component::HeatExchanger(v) => (*v).create_schema_heat_exchanger()
        };
        let result = sqlx::query(qry.as_str()).execute(&temp_pool).await;
        temp_pool.close().await;
        return result;
    }
    pub async fn query(&self, query: String) -> Result<SqliteQueryResult, sqlx::Error> {
        sqlx::query(query.as_str()).execute(&self.pool).await
    }
    // ..
}

pub async fn sqlite_main_twostreamhx() {
    // let db_uri = "sqlite://data/components/heat_exchanger/twostreamhx.db";
    // let comp = interface_SQLite::open(&db_uri).await;
    let mut hx001 = HeatExchanger::new(2, String::from("test")).await;
    hx001.open_new().await;
    let test_csv: CSV = CSV::new("./data/components/heat_exchanger/test.csv");
    let data_csv: Vec<Vec<Data>> = test_csv.load_self_data();
    let mut data: Vec<Stream> = Vec::new();
    // for (_, item) in data_csv.iter().enumerate() {
    //     data.push(Stream::new(
    //         Time::SQL(item[0].clone()),
    //         Pressure::Pascal(item[1].clone()),
    //         Massflow::GramPerSecond(item[2].clone()),
    //         Temperature::Kelvin(item[3].clone()),
    //         Temperature::Kelvin(item[4].clone())
    //     ));
    // }
    data.push(Stream::new(
        Pressure::Pascal(data_csv[1][0].clone()),
        Massflow::GramPerSecond(data_csv[2][0].clone()),
        Temperature::Kelvin(data_csv[3][0].clone()),
        Temperature::Kelvin(data_csv[4][0].clone())
    ));
    data.push(Stream::new(
        Pressure::Pascal(data_csv[1][0].clone()),
        Massflow::GramPerSecond(data_csv[2][0].clone()),
        Temperature::Kelvin(data_csv[3][0].clone()),
        Temperature::Kelvin(data_csv[4][0].clone())
    ));
    let streams: Streams = Streams::new(Time::SQL(data_csv[0][0].clone()), data);
    hx001.add_data(streams).await;
    hx001.close().await;
}
