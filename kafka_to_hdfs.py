from kafka import KafkaConsumer
import json
import pyarrow as pa
import pyarrow.parquet as pq
import os
from datetime import datetime

consumer = KafkaConsumer(
    'traffic-events',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda v: json.loads(v)
)

batch = []
batch_size = 100  # écrire tous les 100 messages

for message in consumer:
    batch.append(message.value)
    if len(batch) >= batch_size:
        now = datetime.now()
        path = f"/data/raw/traffic/year={now.year}/month={now.month}/day={now.day}/"
        os.makedirs(path, exist_ok=True)
        table = pa.Table.from_pylist(batch)
        pq.write_table(table, f"{path}/traffic_{now.timestamp()}.parquet")
        batch = []
        print(f"Wrote {batch_size} records to {path}")