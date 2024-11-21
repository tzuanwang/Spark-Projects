from pyspark.sql import SparkSession

spark = SparkSession. \
    builder. \
    appName("S3 reading"). \
    getOrCreate()

data = spark.read.csv("s3a://de-batch-oct2024/data/Employee_Department.csv")


output_path = "" # define your own output path
data.write.csv(output_path)

spark.stop()