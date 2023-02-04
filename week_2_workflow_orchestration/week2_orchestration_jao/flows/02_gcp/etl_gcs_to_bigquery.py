

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
def transform_parquet(gcs_path: Path) -> pd.DataFrame:
    """Transform data in parquet file"""
    df = pd.read_parquet(gcs_path)
    print(f"pre: missing passenger count: {df['passenger_count'].isna().sum()}")
    df['passenger_count'].fillna(0, inplace=True)
    print(f"post: missing passenger count: {df['passenger_count'].isna().sum()}")
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




# main flow
@flow()
def etl_gcs_to_bigquery() -> None:           #  "--> None means no arguments"
    """The main ETL to load GCS to BigQuery function"""         # example of docstring
    # hardcoding variables for now
    taxi_colour = "yellow"
    year = 2021
    month = 1

    gcs_path = extract_from_gcs(taxi_colour, year, month)
    df = transform_parquet(gcs_path)
    write_bigquery(df)





#main method
if __name__ == '__main__':
    etl_gcs_to_bigquery()