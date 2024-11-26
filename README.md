
1. Start Docker
docker-compose -f docker-compose.yml up -d

2. Send the data
python3 fetch_data.py

3. Listen for it like this
docker exec -it kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic topic1 --from-beginning


Create the topics
3. docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --create --topic topic1 --partitions 1 --replication-factor 1