#!/usr/bin/env python
# coding: utf-8

import os                               # to download csv
import argparse                         #for creating arguments
import pandas as pd
from sqlalchemy import create_engine
from time import time
from datetime import timedelta
from prefect import flow, task
from prefect.tasks import task_input_hash
from prefect_sqlalchemy import SqlAlchemyConnector


@task(log_prints=True, retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def _01_download_data(csv_url):

    if csv_url.endswith(".gz"):
        csv_name = 'output.csv.gz'
    else:
        csv_name = 'output.csv'
    #chunk_size = 100000

    #download csv
    os.system(f"wget {csv_url} -O {csv_name}")
    
    # create an iterator with a chunksize of 100,000, 
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    # to get next element from iterator
    df = next(df_iter)

    #convert "date" columns to "TIMESTAMP".  TODO: maybe put into function.  or loop for cols endwith "datetime" and convert
    if 'tpep_pickup_datetime' in df.columns:
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    if 'tpep_dropoff_datetime' in df.columns:
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    if 'lpep_pickup_datetime' in df.columns:
        df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    if 'lpep_dropoff_datetime' in df.columns:
        df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
    
    return df


@task(log_prints=True)
def _02_remove_passenger_count_zero(df):
    print(f"pre: missing passenger count: {df['passenger_count'].isin([0]).sum()}")
    df = df[df['passenger_count'] != 0]
    print(f"post: missing passenger count: {df['passenger_count'].isin([0]).sum()}")
    return df



@task(log_prints=True, retries=3)
def _99_ingest_data(tablename, df):

    #create the database connection 
    #engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{database}')
    #using sqlalchemyconnector - block in prefect

    #with SqlAlchemyConnector.load("postgres-connector") as database_block:

    connection_block = SqlAlchemyConnector.load("postgres-connector")
    with connection_block.get_connection(begin=False) as engine:
        df.head(n=0).to_sql(name=tablename, con=engine, if_exists='replace')
        print('table:', tablename, 'created.')

        # running in the first 100K rows
        df.to_sql(name=tablename, con=engine, if_exists='append')
        print('first chunk inserted.')


#example of subflow
@flow(name="Subflow", log_prints=True)
def log_subflow(tablename:str):
    print("Logging Subflow for: {tablename}")


#paremetization
@flow(name="Ingest Data Flow")
def ingest_data_flow(tablename:str):
    csv_url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"
    log_subflow(tablename)
    raw_data = _01_download_data(csv_url)
    data = _02_remove_passenger_count_zero(raw_data)
    _99_ingest_data(tablename, data)


#main method
if __name__ == '__main__':
    ingest_data_flow("yellow_taxi_data")