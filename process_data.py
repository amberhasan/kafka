from pyspark.sql import SparkSession

def read_from_kafka(topic, bootstrap_servers="localhost:9092"):
    """
    Read messages from a Kafka topic and print them to the console.

    Args:
        topic (str): The Kafka topic to read messages from.
        bootstrap_servers (str): Kafka bootstrap servers.
    """
    try:
        # Initialize Spark Session
        spark = SparkSession.builder \
            .appName("KafkaReader") \
            .getOrCreate()

        # Read from Kafka
        df = spark.readStream.format("kafka") \
            .option("kafka.bootstrap.servers", bootstrap_servers) \
            .option("subscribe", topic) \
            .load()

        # Select and cast the value column as a string
        messages = df.selectExpr("CAST(value AS STRING) as message")

        # Print messages to the console
        query = messages.writeStream \
            .outputMode("append") \
            .format("console") \
            .start()

        query.awaitTermination()

    except Exception as e:
        print(f"Failed to read from Kafka: {e}")

if __name__ == "__main__":
    # Example usage
    source_topic = "topic1"
    read_from_kafka(source_topic)
