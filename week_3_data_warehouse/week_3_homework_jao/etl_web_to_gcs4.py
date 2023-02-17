# copy file from web, clean up datatype (simple transform), save file as parquet, move to google cloud storage

from pathlib import Path 
import pandas as pd
import os
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket



@task(log_prints=True)                                                                 # decorators which captures infor in prefect.  if excluded then no data in prefect
def fetch(dataset_url: str) -> pd.DataFrame:                            #dtype being returned DataFrame, Path, None.....
    """Read data from web into pandas DataFrame"""
    
    df = pd.read_csv(dataset_url)
    if 'tpep_pickup_datetime' in df.columns:
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    if 'tpep_dropoff_datetime' in df.columns:
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    if 'lpep_pickup_datetime' in df.columns:
        df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    if 'lpep_dropoff_datetime' in df.columns:
        df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
    if 'PUlocationID' in df.columns:
        df["PUlocationID"] = df["PUlocationID"].astype(float)
    if 'DOlocationID' in df.columns:
        df["DOlocationID"] = df["PUlocationID"].astype(float)
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

 
@task()
def delete_local(path: Path) -> None:
    """Delete local files"""

    os.remove(f"{path}")
    return



@flow(name="SubFlow")
def etl_web_to_gcs(taxi_colour:str, year: int, month: int) -> None:           #  "--> None means no arguments"
    """The Subflow"""         # example of docstring
    dataset_file = f"{taxi_colour}_tripdata_{year}-{month:02}"          # yyellow_tripdata_2021-01.csv.gz
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{taxi_colour}/{dataset_file}.csv.gz"

    df_fetch = fetch(dataset_url)            # fetch function task is then created above
    local_path = write_local(df_fetch, taxi_colour, dataset_file)
    write_gcs(local_path)
    delete_local(local_path)

# main flow
@flow(name="ParentFlow")
def etl_parent_flow(
    taxi_colour: str = "fhv",
    year: int = 2020, 
    months: list[int] = [1,2]
):

    for month in months:
        etl_web_to_gcs(taxi_colour, year, month)


#main method
if __name__ == '__main__':
    taxi_colour = "fhv"
    year = 2019
    months = [1,2,3,4,5,6,7,8,9,10,11,12]
    etl_parent_flow(taxi_colour, year, months)




