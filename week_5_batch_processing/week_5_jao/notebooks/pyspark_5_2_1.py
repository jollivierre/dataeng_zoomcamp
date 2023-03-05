
import pyspark
pyspark.__version__

pyspark.__file__


from pyspark.sql import SparkSession


spark = SparkSession.builder \
     .master("local[*]") \
     .appName('test') \
     .getOrCreate()


get_ipython().system('wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv')


get_ipython().system('head -20 taxi+_zone_lookup.csv')


# use spark to read file into dataframe
df = spark.read.csv('taxi+_zone_lookup.csv')


# alternative to read file which loads headers
df = spark.read \
    .option("header", "true") \
     .csv('taxi+_zone_lookup.csv')


df.show()


# test writing file - this created a folder called zones with two files - parquet file and "success" file
df.write.parquet('zones')


get_ipython().system('ls -h zones')


get_ipython().system('head -1 zones/part-00000-88e3c429-a3e4-4051-ada3-cd98fbc705e7-c000.snappy.parquet')

