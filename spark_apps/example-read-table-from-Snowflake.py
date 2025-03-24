import os
from pyspark.sql import SparkSession

spark = SparkSession. \
    builder. \
    appName("Snowflake reading"). \
    getOrCreate()

# make sure to set the following environment variables in .env.spark before your docker-compose up
sf_options = {
    "sfURL": os.getenv("SNOWFLAKE_URL"),
    "sfUser": os.getenv("SNOWFLAKE_USER"),
    "sfPassword": os.getenv("SNOWFLAKE_PASSWORD"),
    "sfDatabase": os.getenv("SNOWFLAKE_DATABASE"),
    "sfSchema": os.getenv("SNOWFLAKE_SCHEMA"),
    "sfWarehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
    "sfRole": os.getenv("SNOWFLAKE_ROLE"),
    "dbtable": os.getenv("SNOWFLAKE_TABLE")
}

# read the data from Snowflake
data = spark.read.format("snowflake") \
    .options(**sf_options) \
    .load()

# test if able to write the data to a new CSV file
output_path = "data/snowflake_test" # this folder should be created in ./data
data.write.csv(output_path)

spark.stop()