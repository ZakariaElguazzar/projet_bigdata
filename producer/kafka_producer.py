from kafka import KafkaProducer
from kafka.errors import KafkaError, NoBrokersAvailable
import json
import time
from traffic_generator import generate_event

producer = None

time.sleep(20)  # Attendre que Kafka démarre

while producer is None:
    try:
        producer = KafkaProducer(
            bootstrap_servers='kafka:9092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            retries=10,
            request_timeout_ms=120000,
            metadata_max_age_ms=30000
        )
        print("Kafka connected")
    except Exception as e:
        print(f"Waiting for Kafka broker... ({e})")
        time.sleep(5)

while True:
    try:
        event = generate_event()
        producer.send('traffic-events', value=event)
        producer.flush()
        print(f"Event sent: {event}")
    

    except KafkaError as e:
        print(f"Kafka error, retrying... {e}")
        time.sleep(5)
