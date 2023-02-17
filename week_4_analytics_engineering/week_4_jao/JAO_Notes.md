--import files into gcs
python ../../week_3_data_warehouse/week_3_homework_jao/etl_web_to_gcs4.py



--
prefect deployment build  ./flows/05_week4_homework/etl_gcs_to_bigquery.py:etl_parent_flow -n "JAO_Homework_Week4" -q default -a




 prefect deployment run ParentFlow_etl_gcs_to_bigquery/JAO_Homework_Week4 --params '{"taxi_colour":"yellow", "year":2019, "months":[1,2,3,4,5,6]}'

 prefect deployment run ParentFlow_etl_gcs_to_bigquery/JAO_Homework_Week4 --params '{"taxi_colour":"yellow", "year":2019, "months":[7,8,9,10,11,12]}'

 prefect deployment run ParentFlow_etl_gcs_to_bigquery/JAO_Homework_Week4 --params '{"taxi_colour":"yellow", "year":2020, "months":[1,2,3,4,5,6]}'

 prefect deployment run ParentFlow_etl_gcs_to_bigquery/JAO_Homework_Week4 --params '{"taxi_colour":"yellow", "year":2020, "months":[7,8,9,10,11,12]}'



 prefect deployment run ParentFlow_etl_gcs_to_bigquery/JAO_Homework_Week4 --params '{"taxi_colour":"green", "year":2019, "months":[1,2,3,4,5,6]}'

 prefect deployment run ParentFlow_etl_gcs_to_bigquery/JAO_Homework_Week4 --params '{"taxi_colour":"green", "year":2019, "months":[7,8,9,10,11,12]}'

 prefect deployment run ParentFlow_etl_gcs_to_bigquery/JAO_Homework_Week4 --params '{"taxi_colour":"green", "year":2020, "months":[1,2,3,4,5,6]}'

 prefect deployment run ParentFlow_etl_gcs_to_bigquery/JAO_Homework_Week4 --params '{"taxi_colour":"green", "year":2020, "months":[7,8,9,10,11,12]}'



--created fhv_tripdata 
 prefect deployment run ParentFlow_etl_gcs_to_bigquery/JAO_Homework_Week4 --params '{"taxi_colour":"fhv", "year":2019, "months":[1,2,3,4,5,6]}'

 prefect deployment run ParentFlow_etl_gcs_to_bigquery/JAO_Homework_Week4 --params '{"taxi_colour":"fhv", "year":2019, "months":[7,8,9,10,11,12]}'