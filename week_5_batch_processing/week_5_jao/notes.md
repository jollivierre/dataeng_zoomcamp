--followed videos
1. installed openjdk
2. installed spark

updated .bashrc with "export" commands


--shows where executable is installed
$which java
$which pyspark

-- show java version
$java --version 


-- show spark version
$spark-shell --version


--to start spark
spark-shell 


--To run PySpark, we first need to add it to PYTHONPATH: - also added to .basrc
-- ensure secoond line is pointing to correct version named file
export PYTHONPATH="${SPARK_HOME}/python/:$PYTHONPATH"
export PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9.5-src.zip:$PYTHONPATH"


-- forwarded port 4040 to see spark interface


--used jupyter notebook - 




-------5_3_1 notes
--this is struct type from scala
StructType([StructField('hvfhs_license_num', StringType(), True), StructField('dispatching_base_num', StringType(), True), StructField('pickup_datetime', StringType(), True), StructField('dropoff_datetime', StringType(), True), StructField('PULocationID', LongType(), True), StructField('DOLocationID', LongType(), True), StructField('SR_Flag', DoubleType(), True)])


-------- needs to be changed into python code
--column names need to be in quotes as they are string
--datatypes must have open/close brackets to invoke
-- "true" should start with capital "T" -- this value at end means the column can be nullable
-- update datatype for pickup/dropoff
-- update datatype for location_ids

StructType([
    StructField('hvfhs_license_num', StringType(), True), 
    StructField('dispatching_base_num', StringType(), True), 
    StructField('pickup_datetime', TimestampType(), True), 
    StructField('dropoff_datetime', TimestampType(), True), 
    StructField('PULocationID', IntegerType(), True), 
    StructField('DOLocationID', IntegerType(), True), 
    StructField('SR_Flag', DoubleType(), True)
])




---5_3_2: SPark dataframes

there are "actions" and " transformations" in spark

transformations - lazy (not executed immediately)
-select columns
-filtering
-joins
-group by


actions - eager (executed immediately)
-show, take, head
-write

