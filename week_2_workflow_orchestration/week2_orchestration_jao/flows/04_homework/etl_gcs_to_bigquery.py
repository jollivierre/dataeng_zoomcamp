

from pathlib import Path 
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials





@task(retries=3)
def extract_from_gcs(taxi_colour: str, year: int, month: int) -> Path:
    """Download parquet trip data from GCS"""
    gcs_path = Path(f"data/{taxi_colour}/{taxi_colour}_tripdata_{year}-{month:02}.parquet")
    gcs_block = GcsBucket.load("dataeng-gcs-jao")
    gcs_block.get_directory(from_path=gcs_path, local_path=f"./")
    return Path(f"{gcs_path}")


@task()
def get_parquet(gcs_path: Path) -> pd.DataFrame:
    """Get parquet file into DataFrame"""
    df = pd.read_parquet(gcs_path)
    return df


@task()
def write_bigquery(df: pd.DataFrame) -> None:
    """Write parquet file to BigQuery"""
    
    gcp_credentials_block = GcpCredentials.load("dataeng-gcp-creds-jao")

    df.to_gbq(
        destination_table="trips_data_all.yellow_tripdata",
        project_id="ny-rides-share-jao",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=100000,
        if_exists="append",
    )


@task(log_prints=True)
def query_tripdata() -> pd.DataFrame:
    """Write BigQuery data to DataFrame"""
    
    gcp_credentials_block = GcpCredentials.load("dataeng-gcp-creds-jao")
    bq_sql = "SELECT count(*) as row_count FROM trips_data_all.yellow_tripdata"

    df_bq = pd.read_gbq(
        bq_sql, 
        project_id = "ny-rides-share-jao", 
        credentials=gcp_credentials_block.get_credentials_from_service_account(), 
        dialect = 'standard'
    ).to_numpy()

    return df_bq



@flow(name="SubFlow_etl_gcs_to_bigquery")
def etl_gcs_to_bigquery(taxi_colour:str, year: int, month: int) -> None:           #  "--> None means no arguments"
    """The ETL to load GCS to BigQuery function"""         # example of docstring

    gcs_path = extract_from_gcs(taxi_colour, year, month)
    df = get_parquet(gcs_path)
    write_bigquery(df)



# main flow
@flow(name="ParentFlow_etl_gcs_to_bigquery", log_prints=True)
def etl_parent_flow(
    taxi_colour: str = "green",
    year: int = 2017, 
    months: list[int] = [12,4]
):

    for month in months:
        etl_gcs_to_bigquery(taxi_colour, year, month)
    
    df_bq_data = query_tripdata()
    print('Rows Processed:', df_bq_data)



#main method
if __name__ == '__main__':
    taxi_colour = "green"
    year = 2017
    months = [12,4]
    etl_parent_flow(taxi_colour, year, months)