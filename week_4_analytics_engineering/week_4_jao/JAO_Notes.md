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





 ---
 dbt run - runs all models
 dbt run -m <model_name> - rund specific model

 create a macro in dbt (same as function) - as .sql file in macros folder

can use packages from dbt package hub (https://hub.getdbt.com/)
packages are imported into a created "packages.yml" (in main directory of project) file by running "dbt debs"
this creates a folder "dbt_packages", if not already present
under this it adds the packages installed 


any model run - user can look at the code actually sent to server in --> target/compiled


varibales can be used like any other program
- in the project.yml it will be a global variable

- variable can also be defined in the CLI to change at run time
e.g. dbt run -m stg_green_tripdata --var 'is_test_run: false'


---in dbt "seeds" are csv files that are in repo.  smaller files with data that will not change frequently
--in this case we want to look at zones
-- added to "seeds" folder
need to run command "dbt seed" -->  this will create table based on csv

--config of seeds can be added to dbt_project.yml
--columns can be defined

-- "dbt seed --full-refresh" --> will drop the table and recreate.  without arugment it will append



--expectation is the "core" folder will be "presentation" layer, thus "tables" should be created
--created a "dim_zones" -- -this is from teh csv
--created a "fact_trips" -- - this is from the two models (yellow and green)




--to run seeds and models
dbt build 

another way to run model and all dependencies - the "+" sign includes dependencies
dbt build --select +fact_trips



***testing and documentation*** added to schema.sql related model folder
unique
not null
accepted values
foreign key
--custom test in the form of a sql query


dbt provides a way to generate documentation and render to website

included in schema.yml for "staging" folder is an example of "accepted values" test for payment_types using a variable which is defined in dbt_project.yml
--done this way because test applies to both "green" and "yellow" data
--"quote: false" is added to test to accept as chars


command to run test by model, or by test_name(if known)
dbt test



**seeds and macros can also be documented



--deploy dbt project
* create job 
* add as many commnads to job
* can create schedule for job