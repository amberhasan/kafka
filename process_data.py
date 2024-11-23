from pyspark.sql import SparkSession

def read_and_write_kafka(input_topic, output_topic):
    # Initialize Spark
    spark = SparkSession.builder \
        .appName("KafkaPipeline") \
        .getOrCreate()

    # Read from topic1
    df = spark.readStream.format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", input_topic) \
        .load()

    # Select and cast the value column as string
    messages = df.selectExpr("CAST(value AS STRING) as message")

    # Write the messages to topic2
    messages.selectExpr("CAST(message AS STRING) as value") \
        .writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("topic", output_topic) \
        .option("checkpointLocation", "/tmp/kafka-checkpoint") \
        .start() \
        .awaitTermination()

if __name__ == "__main__":
    input_topic = "topic1"
    output_topic = "topic2"
    read_and_write_kafka(input_topic, output_topic)
