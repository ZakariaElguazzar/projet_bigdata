from kafka import KafkaProducer
import json
import time
from traffic_generator import generate_event

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

while True:
    event = generate_event()
    producer.send('traffic-events', value=event)
    print(f"Event sent: {event}")
    time.sleep(1)
