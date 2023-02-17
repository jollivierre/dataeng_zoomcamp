--create external table
CREATE OR REPLACE EXTERNAL TABLE `ny-rides-share-jao.trips_data_all.fhv_tripdata_csv_ext_gcs`
  OPTIONS(
    format ="CSV",
    uris = ['gs://de_data_lake_jao_ny-rides-share-jao/data/fhv/fhv_tripdata_2019-*.csv.gz']
    );


--create table
CREATE OR REPLACE TABLE `ny-rides-share-jao.trips_data_all.fhv_tripdata_csv_nonpartitioned`
AS SELECT * FROM `ny-rides-share-jao.trips_data_all.fhv_tripdata_csv_ext_gcs`;


--Implement the optimized solution you chose for question 4.
CREATE OR REPLACE TABLE `ny-rides-share-jao.trips_data_all.fhv_tripdata_csv_partitioned`
PARTITION BY DATE(pickup_datetime)
CLUSTER BY Affiliated_base_number AS (
  SELECT * FROM `ny-rides-share-jao.trips_data_all.fhv_tripdata_csv_ext_gcs`
);




--parquet files
--create external table
CREATE OR REPLACE EXTERNAL TABLE `ny-rides-share-jao.trips_data_all.fhv_tripdata_parquet_ext_gcs`
  OPTIONS(
    format ="PARQUET",
    uris = ['gs://de_data_lake_jao_ny-rides-share-jao/data/fhv/fhv_tripdata_2019-*.parquet']
    );



--create table
CREATE OR REPLACE TABLE `ny-rides-share-jao.trips_data_all.fhv_tripdata_parquet_nonpartitioned`
AS SELECT * FROM `ny-rides-share-jao.trips_data_all.fhv_tripdata_parquet_ext_gcs`;

