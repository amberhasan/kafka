from pyspark.sql import SparkSession
import requests
import json

def read_kafka_and_write_elasticsearch(input_topic, es_index):
    # Initialize Spark
    spark = SparkSession.builder \
        .appName("KafkaToElasticsearch") \
        .getOrCreate()

    # Read from topic1
    df = spark.readStream.format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", input_topic) \
        .load()

    # Select and cast the value column as string
    messages = df.selectExpr("CAST(value AS STRING) as message")

    def send_to_elasticsearch(partition):
        es_url = f"http://localhost:9200/{es_index}/_doc/"
        for row in partition:
            doc = {"message": row["message"]}
            response = requests.post(es_url, json=doc)
            if response.status_code not in (200, 201):
                print(f"Failed to index: {response.text}")

    # Write messages to Elasticsearch
    messages.writeStream \
        .foreachBatch(lambda batch_df, _: batch_df.foreachPartition(send_to_elasticsearch)) \
        .start() \
        .awaitTermination()

if __name__ == "__main__":
    input_topic = "topic1"
    es_index = "topic1-index"  # Your Elasticsearch index
    read_kafka_and_write_elasticsearch(input_topic, es_index)
