from pyspark.sql import SparkSession

# Initialize Spark
spark = SparkSession.builder \
    .appName("TestKafkaWrite") \
    .getOrCreate()

# Create a simple DataFrame with one message
test_df = spark.createDataFrame([("Test message for topic2",)], ["value"])

# Write the message to topic2
test_df.selectExpr("CAST(value AS STRING) as value") \
    .write \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("topic", "topic2") \
    .save()

print("Message successfully written to topic2!")
