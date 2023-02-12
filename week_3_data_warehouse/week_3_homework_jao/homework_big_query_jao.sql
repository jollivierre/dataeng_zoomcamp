--create external table
CREATE OR REPLACE EXTERNAL TABLE `ny-rides-share-jao.trips_data_all.ext_gcs_fhv_tripdata`
  OPTIONS(
    format ="CSV",
    uris = ['gs://de_data_lake_jao_ny-rides-share-jao/data/fhv/fhv_tripdata_2019-*.csv.gz']
    );


--What is the count for fhv vehicle records for year 2019?
SELECT count(*) FROM `ny-rides-share-jao.trips_data_all.ext_gcs_fhv_tripdata`;


--create table
CREATE OR REPLACE TABLE `ny-rides-share-jao.trips_data_all.nonpartitioned_fhv_tripdata`
AS SELECT * FROM `ny-rides-share-jao.trips_data_all.ext_gcs_fhv_tripdata`;


--Write a query to count the distinct number of affiliated_base_number for the entire dataset on both the tables.
SELECT 'ext_gcs_fhv_tripdata', count(distinct Affiliated_base_number) 
FROM `ny-rides-share-jao.trips_data_all.ext_gcs_fhv_tripdata`;

SELECT 'ext_gcs_fhv_tripdata', count(distinct Affiliated_base_number) 
FROM `ny-rides-share-jao.trips_data_all.nonpartitioned_fhv_tripdata`;



--How many records have both a blank (null) PUlocationID and DOlocationID in the entire dataset?
SELECT count(*) 
FROM `ny-rides-share-jao.trips_data_all.ext_gcs_fhv_tripdata`
WHERE (PUlocationID is null
AND DOlocationID is null);


--Implement the optimized solution you chose for question 4.
CREATE OR REPLACE TABLE `ny-rides-share-jao.trips_data_all.partitioned_fhv_tripdata`
PARTITION BY DATE(pickup_datetime)
CLUSTER BY Affiliated_base_number AS (
  SELECT * FROM `ny-rides-share-jao.trips_data_all.ext_gcs_fhv_tripdata`
);



--Write a query to retrieve the distinct affiliated_base_number between pickup_datetime 2019/03/01 and 2019/03/31 (inclusive).
SELECT distinct Affiliated_base_number
FROM `ny-rides-share-jao.trips_data_all.nonpartitioned_fhv_tripdata`
WHERE date(pickup_datetime) between '2019-03-01' and '2019-03-31';
--estimated 647.87mb

SELECT distinct Affiliated_base_number
FROM `ny-rides-share-jao.trips_data_all.partitioned_fhv_tripdata`
WHERE date(pickup_datetime) between '2019-03-01' and '2019-03-31';
--estimated 23.05mb



--parquet files
--create external table
CREATE OR REPLACE EXTERNAL TABLE `ny-rides-share-jao.trips_data_all.ext_gcs_fhv_tripdata_parquet`
  OPTIONS(
    format ="PARQUET",
    uris = ['gs://de_data_lake_jao_ny-rides-share-jao/data/fhv/fhv_tripdata_2019-*.parquet']
    );


--What is the count for fhv vehicle records for year 2019?
SELECT count(*) FROM `ny-rides-share-jao.trips_data_all.ext_gcs_fhv_tripdata_parquet`;


--create table
CREATE OR REPLACE TABLE `ny-rides-share-jao.trips_data_all.nonpartitioned_fhv_tripdata_parquet`
AS SELECT * FROM `ny-rides-share-jao.trips_data_all.ext_gcs_fhv_tripdata_parquet`;

