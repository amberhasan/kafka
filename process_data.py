from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf, to_json, struct, explode, current_timestamp
from pyspark.sql.types import StringType, ArrayType
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Define a UDF to extract named entities
def extract_entities(text):
    doc = nlp(text)
    return [ent.text for ent in doc.ents]

extract_entities_udf = udf(extract_entities, ArrayType(StringType()))

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

    # Extract named entities
    entities = messages.withColumn("entities", extract_entities_udf(col("message")))

    # Explode entities into rows and add a timestamp column
    exploded_entities = entities.select(
        explode(col("entities")).alias("entity"),
        current_timestamp().alias("timestamp")  # Add a timestamp column
    )

    # Add watermark and perform aggregation
    entity_counts = exploded_entities \
        .withWatermark("timestamp", "10 minutes") \
        .groupBy("entity") \
        .count()

    # Convert entity counts to JSON format
    output_data = entity_counts.select(to_json(struct(col("entity"), col("count"))).alias("value"))

    # Write the processed data to topic2
    output_data.writeStream \
        .outputMode("update") \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("topic", output_topic) \
        .option("checkpointLocation", "/tmp/kafka-checkpoint-entity-count") \
        .start() \
        .awaitTermination()

if __name__ == "__main__":
    input_topic = "topic1"
    output_topic = "topic2"
    read_and_write_kafka(input_topic, output_topic)
