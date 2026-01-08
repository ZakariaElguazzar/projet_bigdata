from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, window
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    DoubleType,
    TimestampType
)

# ================================
# 1. Spark Session
# ================================
spark = (
    SparkSession.builder
    .appName("TrafficAnalysisStreaming")
    .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:8020")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

# ================================
# 2. Schema
# ================================
schema = StructType([
    StructField("sensor_id", StringType(), True),
    StructField("road_type", StringType(), True),
    StructField("zone", StringType(), True),
    StructField("road_id", StringType(), True),
    StructField("vehicle_count", IntegerType(), True),
    StructField("average_speed", DoubleType(), True),
    StructField("occupancy_rate", DoubleType(), True),
    StructField("event_time", TimestampType(), True)
])

# ================================
# 3. Read streaming from HDFS
# ================================
df = (
    spark.readStream
    .schema(schema)
    .json("hdfs://namenode:8020/data/raw/traffic/")
)

# ================================
# 4. Trafic moyen par zone (WINDOW)
# ================================
traffic_zone = (
    df
    .withWatermark("event_time", "2 minutes")
    .groupBy(
        window(col("event_time"), "2 minutes"),
        col("zone")
    )
    .agg(avg("vehicle_count").alias("avg_vehicle_count"))
)


# ================================
# 5. Vitesse moyenne par route (WINDOW)
# ================================
speed_route = (
    df
    .withWatermark("event_time", "2 minutes")
    .groupBy(
        window(col("event_time"), "2 minutes"),
        col("road_id")
    )
    .agg(avg("average_speed").alias("avg_speed"))
)


# ================================
# 6. Zones congestionnées
# ================================
congestion_zones = (
    df
    .filter(col("occupancy_rate") > 70)
    .withWatermark("event_time", "2 minutes")
    .groupBy(
        window(col("event_time"), "2 minutes"),
        col("zone")
    )
    .count()
)


# ================================
# 7. Write streaming to HDFS (APPEND)
# ================================
traffic_zone_query = (
    traffic_zone.writeStream
    .outputMode("append")
    .format("json")
    .option("path", "hdfs://namenode:8020/data/processed/traffic/traffic_zone")
    .option("checkpointLocation", "hdfs://namenode:8020/checkpoints/traffic_zone")
    .trigger(processingTime="1 minute")
    .start()
)

speed_route_query = (
    speed_route.writeStream
    .outputMode("append")
    .format("json")
    .option("path", "hdfs://namenode:8020/data/processed/traffic/speed_route")
    .option("checkpointLocation", "hdfs://namenode:8020/checkpoints/speed_route")
    .trigger(processingTime="1 minute")
    .start()
)


congestion_query = (
    congestion_zones.writeStream
    .outputMode("append")
    .format("json")
    .option("path", "hdfs://namenode:8020/data/processed/traffic/congestion")
    .option("checkpointLocation", "hdfs://namenode:8020/checkpoints/congestion")
    .trigger(processingTime="1 minute")
    .start()
)

debug_query = (
    df.writeStream
    .outputMode("append")
    .format("console") # Affiche les données brutes dans votre terminal
    .start()
)


# ================================
# 8. Await termination
# ================================
spark.streams.awaitAnyTermination()
