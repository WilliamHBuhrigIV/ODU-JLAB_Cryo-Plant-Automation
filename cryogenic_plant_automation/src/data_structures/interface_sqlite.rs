use sqlx::{sqlite::SqliteQueryResult, Sqlite, SqlitePool, migrate::MigrateDatabase};

async fn create_schema_twostreamhx(db_url: &str) -> Result<SqliteQueryResult, sqlx::Error>{
    let pool = SqlitePool::connect(&db_url).await?;
    let qry = 
    "PRAGMA foreign_keys = ON;
    CREATE TABLE IF NOT EXISTS component (
        component_name TEXT PRIMARY KEY NOT NULL,
        component_type TEXT NOT NULL,
        input_output_number BLOB NOT NULL,
        processed_number BLOB DEFAULT 0,
        update_on DATETIME DEFAULT (datetime('now','localtime'))
    );
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
    );
    CREATE TABLE IF NOT EXISTS process (
        process_id INTEGER PRIMARY KEY AUTOINCREMENT,
        a INTEGER NOT NULL
    );";
    let result = sqlx::query(&qry).execute(&pool).await;
    pool.close().await;
    return result;
}

pub async fn sqlite_main_twostreamhx() {
    let db_url = String::from("sqlite://data/components/twostreamhx.db");
    if !Sqlite::database_exists(&db_url).await.unwrap_or(false){
        Sqlite::create_database(&db_url).await.unwrap();
        match create_schema_twostreamhx(&db_url).await{
            Ok(_) => println!("DB Created"),
            Err(e) => panic!("{}",e)
        }
    }
    let instances = SqlitePool::connect(&db_url).await.unwrap();
    let qry = "
        INSERT INTO component (component_name, component_type, input_output_number, processed_number) Values( 'test', 'HeatExchanger', '8', '0' );
        --UPDATE component SET update_on = datetime('now','localtime');--
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
        );
        --INSERT INTO process (a) Values('12');--
    ";
    let result = sqlx::query(&qry).execute(&instances).await;
    instances.close().await;
    println!("{:?}",result);
}
