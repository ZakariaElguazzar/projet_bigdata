from kafka import KafkaConsumer
import json
import pyarrow as pa
import pyarrow.parquet as pq
from pyarrow import fs
from datetime import datetime

# -----------------------------
# Kafka Consumer
# -----------------------------
consumer = KafkaConsumer(
    'traffic-events',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda v: json.loads(v)
)

hdfs = fs.HadoopFileSystem(
    host="namenode",
    port=8020
)

batch = []
batch_size = 10

for message in consumer:
    batch.append(message.value)

    if len(batch) >= batch_size:
        now = datetime.now()

        hdfs_path = (
            f"/data/raw/traffic/"
            f"year={now.year}/month={now.month}/day={now.day}/"
            f"traffic_{int(now.timestamp())}.parquet"
        )

        table = pa.Table.from_pylist(batch)

        # Write Parquet directly to HDFS
        with hdfs.open_output_stream(hdfs_path) as f:
            pq.write_table(table, f)

        print(f"✔ Written to HDFS: {hdfs_path}")

        batch = []
