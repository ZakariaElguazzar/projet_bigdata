from kafka import KafkaConsumer
from hdfs import InsecureClient
from datetime import datetime
import json

consumer = KafkaConsumer(
    'traffic-events',
    bootstrap_servers='kafka:29092',
    value_deserializer=lambda v: json.loads(v)
)

client = InsecureClient('http://namenode:9870', user='hadoop')

for message in consumer:
    now = datetime.now()
    path = f"/data/raw/traffic/{now.timestamp()}.json"

    client.write(
        path,
        data=json.dumps(message.value),
        overwrite=True
    )

    print(f"✔ Written to HDFS: {path}")



'''import pyarrow as pa
import pyarrow.parquet as pq
from hdfs import InsecureClient
import json
from datetime import datetime

client = InsecureClient('http://namenode:9870', user='hadoop')

records = []

# Collect messages from Kafka
for message in consumer:
    records.append(message.value)
    if len(records) >= 100:  # batch write for efficiency
        table = pa.Table.from_pylist(records)
        path = f"/data/processed/traffic/speed_route/{datetime.now().timestamp()}.parquet"
        
        with client.write(path, overwrite=True) as f:
            pq.write_table(table, f)
        
        print(f"✔ Written Parquet to HDFS: {path}")
        records = []'''
