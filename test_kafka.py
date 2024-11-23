from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092')
print("KafkaProducer initialized successfully!")
