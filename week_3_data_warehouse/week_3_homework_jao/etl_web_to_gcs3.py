# copy file from web, clean up datatype (simple transform), save file as parquet, move to google cloud storage

from pathlib import Path 
import pandas as pd
import os
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket


@task(log_prints=True)
def download_write_local(dataset_url: str, taxi_colour: str, dataset_file: str) -> Path:
    """Download GZIP files and save locally"""

    path = Path(f"data/{taxi_colour}/{dataset_file}.csv.gz")
    os.system(f"wget {dataset_url} -O {path}")
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

    local_path = download_write_local(dataset_url, taxi_colour, dataset_file)
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




