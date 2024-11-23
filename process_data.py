from pyspark.sql import SparkSession
import logging

# Set up logging for better debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("KafkaWrite")

def write_to_kafka(message, topic, bootstrap_servers="localhost:9092"):
    """
    Write a simple message to a Kafka topic.

    Args:
        message (str): The message to send to Kafka.
        topic (str): The Kafka topic to send the message to.
        bootstrap_servers (str): Kafka bootstrap servers.
    """
    try:
        # Initialize Spark Session
        spark = SparkSession.builder \
            .appName("KafkaMessageWriter") \
            .getOrCreate()

        # Create a DataFrame with the provided message
        message_df = spark.createDataFrame([(message,)], ["value"])

        # Write the message to the specified Kafka topic
        message_df.selectExpr("CAST(value AS STRING) as value") \
            .write \
            .format("kafka") \
            .option("kafka.bootstrap.servers", bootstrap_servers) \
            .option("topic", topic) \
            .save()

        logger.info(f"Message successfully written to topic '{topic}': {message}")
        print(f"Message successfully written to topic '{topic}': {message}")

    except Exception as e:
        logger.error(f"Failed to write to Kafka: {e}")
        print(f"Failed to write to Kafka: {e}")
    finally:
        # Stop the Spark session to release resources
        spark.stop()

if __name__ == "__main__":
    # Example usage
    test_message = "Improved test message for topic2"
    target_topic = "topic2"

    write_to_kafka(test_message, target_topic)
