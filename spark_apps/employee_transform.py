from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("Employee Aggregation and Grouping") \
    .getOrCreate()

# Load the Employee data
employee_path = "data/employees.csv"
employees_df = spark.read.option("header", "true").csv(employee_path)

# Load the Department data
department_path = "data/department.csv"
departments_df = spark.read.option("header", "true").csv(department_path)

# Convert salary column to double for aggregation
employees_df = employees_df.withColumn("salary", col("salary").cast("double"))

# Join employees with departments
joined_df = employees_df.join(departments_df, employees_df.department == departments_df.dept_name)

# Group by department and calculate average salary and employee count
aggregated_df = joined_df.groupBy("dept_name", "location") \
    .agg(
        avg("salary").alias("avg_salary"),
        count("id").alias("employee_count")
    )

# Show results
aggregated_df.show()

# Write aggregated results to a new CSV file
output_path = "data/aggregated_department_data"
aggregated_df.write.option("header", "true").csv(output_path)

# Stop the Spark session
spark.stop()
