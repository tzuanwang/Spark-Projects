from pyspark.sql import SparkSession

spark = SparkSession. \
    builder. \
    appName("S3 reading"). \
    getOrCreate()

data = spark.read.csv("s3a://de-batch-oct2024/data/Employee_Department.csv")


output_path = "data/s3_test" # this folder should be created in ./data
data.write.csv(output_path)

spark.stop()