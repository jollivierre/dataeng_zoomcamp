#!/usr/bin/env python
# coding: utf-8

import os                               # to download csv
import argparse                         #for creating arguments
import pandas as pd
from sqlalchemy import create_engine
from time import time
#gzip -d yellow_tripdata_2021-01.csv.gz 

def main(params):
    username = params.username
    password = params.password
    host = params.host
    port = params.port
    database = params.database
    tablename = params.tablename
    csv_url = params.csv_url
    csv_name = 'output.csv'

    #download csv
    os.system(f"wget {csv_url} -O {csv_name}")
    
    #create the database connection 
    engine = create_engine('postgresql://{username}:{password}@{host}:{port}/{database}')

    # create an iterator with a chunksize of 100,000, 
    df_iter = pd.read_csv('csv_name', iterator=True, chunksize=100000)

    # to get next element from iterator
    df = next(df_iter)

    #convert "date" columns to "TIMESTAMP"
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)


    # using this command to generate and run the "create table statement" on the fly
    # n=0 to show only header row
    # command will create the table and insert "all" the rows, but because n=0 is specified only the table is created
    # check using \dt 
    df.head(n=0).to_sql(name='{tablename}', con=engine, if_exists='replace')


    # running in the first 100K rows
    df.to_sql(name='{tablename}', con=engine, if_exists='append')


    #simple while loop to import data 100K at a time
    #loop wiil run until no more rows to insert
    while True:
        t_start = time()
        
        df = next(df_iter)
        
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        
        df.to_sql(name='{tablename}', con=engine, if_exists='append')
        
        t_end = time()
        
        print('inserted another chunk....time taken: %.3f second' % (t_end - t_start))



#main method
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    # arguments: user, pw, host, port, database, table name, url of the csv

    parser.add_argument('--username', help='username for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host/server for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--database', help='database for postgres')
    parser.add_argument('--tablename', help='tablename for postgres')
    parser.add_argument('--csv_url', help='csv_url for postgres')

    args = parser.parse_args()
    main(args)

#print(args.accumulate(args.integers))




