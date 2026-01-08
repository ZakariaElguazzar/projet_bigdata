from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'traffic-events',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda v: json.loads(v)
)

for message in consumer:
    print(f"Received: {message.value}")




