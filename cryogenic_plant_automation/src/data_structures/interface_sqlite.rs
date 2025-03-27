use sqlx::{migrate::MigrateDatabase, sqlite::SqliteQueryResult, Pool, Sqlite, SqlitePool};

#[allow(non_camel_case_types)]
pub struct interface_SQLite {
    db_uri: &'static str,
    pool: Pool<Sqlite>
}

#[allow(dead_code)]
impl interface_SQLite {
    pub async fn new(db_uri: &'static str) -> Self { Self {
        db_uri,
        pool: {
            if !Sqlite::database_exists(&db_uri).await.unwrap_or(false) {
                Sqlite::create_database(&db_uri).await.unwrap();
                match Self::create_schema(&db_uri).await{
                    Ok(_) => (),
                    Err(e) => panic!("{:?}",e)
                }
            }
            SqlitePool::connect(&db_uri).await.unwrap()
        }
    }}
    // Panic if Database doesn't exists
    pub async fn open(db_uri: &'static str) -> Self { Self {
        db_uri,
        pool: {
            match Sqlite::database_exists(&db_uri).await {
                Ok(true) => match SqlitePool::connect(&db_uri).await {
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
    pub async fn create_schema(db_url: &str) -> Result<SqliteQueryResult, sqlx::Error>{
        let temp_pool = SqlitePool::connect(&db_url).await?;

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
        qry.insert_str(qry.len(),"
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
        qry.insert_str(qry.len(), "
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

        let qry = qry.as_str(); // Squishes mut String into !mut &str
        let result = sqlx::query(&qry).execute(&temp_pool).await;
        temp_pool.close().await;
        return result;
    }
    pub async fn add_data(&self) -> Result<SqliteQueryResult, sqlx::Error> {
        let qry = "
            UPDATE component SET update_on = datetime('now','localtime');
            INSERT INTO data (
                time,
                pressure_stream_1,
                pressure_stream_2,
                massflow_stream_1,
                massflow_stream_2,
                temperature_stream_1_inlet,
                temperature_stream_1_outlet,
                temperature_stream_2_inlet,
                temperature_stream_2_outlet
            ) Values(
                datetime('now','localtime'),
                '101325',
                '101325',
                '18.003',
                '18.003',
                '300',
                '200',
                '200',
                '300'
            );"
        ;
        sqlx::query(&qry).execute(&self.pool).await
    }
    // ..
}

pub async fn sqlite_main_twostreamhx() {
    let db_uri = "sqlite://data/components/heat_exchanger/twostreamhx.db";
    let comp = interface_SQLite::open(&db_uri).await;
    _ = comp.add_data().await;
    comp.close().await;
}
