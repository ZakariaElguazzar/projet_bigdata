from kafka import KafkaConsumer
from hdfs import InsecureClient
from datetime import datetime
import json
import time

time.sleep(20)  # Attendre que Kafka et HDFS démarrent

consumer = KafkaConsumer(
    'traffic-events',
    bootstrap_servers='kafka:9092',
    value_deserializer=lambda v: json.loads(v),
    auto_offset_reset='earliest',   # pour lire depuis le début
    enable_auto_commit=True,
    group_id='traffic-hdfs-consumer'
)

client = InsecureClient('http://namenode:9870', user='hadoop')

print("Consumer started, waiting for messages...")

while True:
    # Récupère les messages disponibles, avec un timeout de 5 secondes
    msg_pack = consumer.poll(timeout_ms=5000)

    if not msg_pack:
        # Aucun message reçu
        print("No messages yet, waiting...")
        time.sleep(2)
        continue

    for tp, messages in msg_pack.items():
        for message in messages:
            now = datetime.now()
            path = f"/data/raw/traffic/{now.timestamp()}.json"

            client.write(
                path,
                data=json.dumps(message.value),
                overwrite=True
            )
            print(f"✔ Written to HDFS: {path}")
