# copy file from web, clean up datatype (simple transform), save file as parquet, move to google cloud storage

from pathlib import Path 
import pandas as pd
import os
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket


@task()                                                                 # decorators which captures infor in prefect.  if excluded then no data in prefect
def fetch(dataset_url: str) -> pd.DataFrame:                            #dtype being returned DataFrame, Path, None.....
    """Read data from web into pandas DataFrame"""
    
    df = pd.read_csv(dataset_url)
    print(df)
    return df

@task(log_prints=True)
def clean(df = pd.DataFrame) -> pd.DataFrame:
    """Convert dtype to datetime"""
    if 'tpep_pickup_datetime' in df.columns:
        df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    if 'tpep_dropoff_datetime' in df.columns:
        df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
    if 'lpep_pickup_datetime' in df.columns:
        df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'])
    if 'lpep_dropoff_datetime' in df.columns:
        df['lpep_dropoff_datetime'] = pd.to_datetime(df['lpep_dropoff_datetime'])

    
    
    print(df.head(2))
    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")
    return df

@task(log_prints=True)
def write_local(df: pd.DataFrame, taxi_colour: str, dataset_file: str) -> Path:
    """Write DataFrame out locally as a parquet file"""
    print("start of failure")
    path = Path(f"week_2_workflow_orchestration/week2_orchestration_jao/data/{taxi_colour}/{dataset_file}.parquet")
    df.to_parquet(path, compression="gzip")                     # pyarrow for gzip updated JAO
    print("end of failure")
    return path

@task()
def write_gcs(path: Path) -> None:
    """Update local parquet file to GCS"""
    gcs_block = GcsBucket.load("dataeng-gcs-jao")
    gcs_block.upload_from_path(from_path=f"{path}", to_path=path)           # if "to_path" excluded then file is uploaded to base folder
    return 


#@task()
#def delete_local(path: Path) -> None:
#    """Delete local parquet file"""

#    os.remove(f"{path}")
#    return


# main flow
@flow()
def etl_web_to_gcs() -> None:           #  "--> None means no arguments"
    """The main ETL function"""         # example of docstring
    # hardcoding variables for now
    taxi_colour = "green"
    year = 2020
    month = 11
    dataset_file = f"{taxi_colour}_tripdata_{year}-{month:02}"          # yyellow_tripdata_2021-01.csv.gz
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{taxi_colour}/{dataset_file}.csv.gz"

    df_fetch = fetch(dataset_url)            # fetch function task is then created above
    df_clean = clean(df_fetch)
    local_path = write_local(df_clean, taxi_colour, dataset_file)
    write_gcs(local_path)
  #  delete_local(local_path)




#main method
if __name__ == '__main__':
    etl_web_to_gcs()



