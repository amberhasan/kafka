from kafka import KafkaConsumer
import requests
import json

# Elasticsearch URL
ELASTIC_URL = "http://localhost:9200"
INDEX = "topic2"  # Elasticsearch index name

# Set up Kafka consumer
consumer = KafkaConsumer(
    'topic2',  # Kafka topic to consume
    bootstrap_servers=['localhost:9092'],  # Your Kafka server
    value_deserializer=lambda x: x.decode('utf-8')  # Decode Kafka messages as strings
)

# Send messages from Kafka to Elasticsearch
for message in consumer:
    # Prepare the data
    doc = {"message": message.value}

    # Send to Elasticsearch
    response = requests.post(
        f"{ELASTIC_URL}/{INDEX}/_doc",
        headers={"Content-Type": "application/json"},
        data=json.dumps(doc)
    )

    if response.status_code in [200, 201]:
        print(f"Document indexed: {response.json()}")
    else:
        print(f"Failed to index document: {response.text}")
