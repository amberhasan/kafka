0. Create the topics
docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --create --topic topic1 --partitions 1 --replication-factor 1

1. Start Docker
docker-compose -f docker-compose.yml up -d

2. Send the data to topic1 
python3 fetch_data.py

3. Listen for topic1 like this
docker exec -it kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic topic1 --from-beginning

4. Call spark like this
 spark-submit \                 
--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3 \
process_data.py

5. Listen for topic2 like this 
docker exec -it kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic topic2 --from-beginning
