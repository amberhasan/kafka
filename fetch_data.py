import time
from kafka import KafkaProducer
import praw

# Reddit setup
reddit = praw.Reddit(
    client_id='4CgzUN1Im44jAtlQNFE1nA',
    client_secret='CIPLD3l-XpRsOhG994V5PH3h7j4n2w',
    user_agent='Kafka-Streamer/1.0'
)

# Kafka setup
producer = KafkaProducer(bootstrap_servers='localhost:9092')


def fetch_and_send():
    try:
        # Access the 'test' subreddit
        subreddit = reddit.subreddit('news')  # Replace 'test' with 'news'
        print("Connected to subreddit. Streaming comments...")

        # Stream comments in real time
        for comment in subreddit.stream.comments(skip_existing=True):
            try:
                # Send comment to Kafka topic 'topic1'
                producer.send('topic1', value=comment.body.encode('utf-8'))
                print(f"Sent to Kafka: {comment.body}")

            except Exception as kafka_error:
                print(f"Error sending comment to Kafka: {kafka_error}")

            # Delay to respect API limits
            time.sleep(1)

    except Exception as e:
        print(f"Failed to fetch or stream comments: {e}")


if __name__ == "__main__":
    fetch_and_send()
