# copy file from web, clean up datatype (simple transform), save file as parquet, move to google cloud storage

from pathlib import Path 
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect.tasks import task_input_hash




@task(retries=3)                                                    # decorators which captures infor in prefect.  if excluded then no data in prefect
def fetch(dataset_url: str) -> pd.DataFrame:                            #dtype being returned DataFrame, Path, None.....
    """Read data from web into pandas DataFrame"""
    
    df = pd.read_csv(dataset_url)
    print(df)
    return df

@task(log_prints=True)
def clean(df = pd.DataFrame) -> pd.DataFrame:
    """Convert dtype to datetime"""
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
    print(df.head(2))
    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")
    return df

@task(log_prints=True)
def write_local(df: pd.DataFrame, taxi_colour: str, dataset_file: str) -> Path:
    """Write DataFrame out locally as a parquet file"""
    path = Path(f"data/{taxi_colour}/{dataset_file}.parquet")
    df.to_parquet(path, compression="gzip")                     # pyarrow for gzip
    return path


@task()
def write_gcs(path: Path) -> None:
    """Update local parquet file to GCS"""
    gcs_block = GcsBucket.load("dataeng-gcs-jao")
    gcs_block.upload_from_path(from_path=f"{path}", to_path=path)           # if "to_path" excluded then file is uploaded to base folder
    return 





@flow(name="SubFlow01")
def etl_web_to_gcs(taxi_colour:str, year: int, month: int) -> None:           #  "--> None means no arguments"
    """The main ETL function"""         # example of docstring
    # hardcoding variables for now
    # taxi_colour = "yellow"
    # year = 2021
    # month = 1
    dataset_file = f"{taxi_colour}_tripdata_{year}-{month:02}"          # yyellow_tripdata_2021-01.csv.gz
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{taxi_colour}/{dataset_file}.csv.gz"

    df_fetch = fetch(dataset_url)            # fetch function task is then created above
    df_clean = clean(df_fetch)
    local_path = write_local(df_clean, taxi_colour, dataset_file)
    write_gcs(local_path)


# parent flow to trigger the above flow for three months
@flow(name="ParentFlow")
def etl_parent_flow(
    taxi_colour: str = "yellow",
    year: int = 2021, 
    months: list[int] = [1,2]
):

    for month in months:
        etl_web_to_gcs(taxi_colour, year, month)



#main method
if __name__ == '__main__':
    taxi_colour = "yellow"
    year = 2021
    months = [1,2,3]
    etl_parent_flow(taxi_colour, year, months)



