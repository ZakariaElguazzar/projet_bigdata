from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType, LongType
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# ======================================
# 1. DEFINITION DES SCHEMAS (MANUELLE)
# ======================================

# Structure commune pour la fenêtre temporelle
window_schema = StructType([
    StructField("start", TimestampType(), True),
    StructField("end", TimestampType(), True)
])

# Schéma pour Traffic Zone
traffic_zone_schema = StructType([
    StructField("window", window_schema, True),
    StructField("zone", StringType(), True),
    StructField("avg_vehicle_count", DoubleType(), True)
])

# Schéma pour Speed Route
speed_route_schema = StructType([
    StructField("window", window_schema, True),
    StructField("road_id", StringType(), True),
    StructField("avg_speed", DoubleType(), True)
])

# Schéma pour Congestion
congestion_schema = StructType([
    StructField("window", window_schema, True),
    StructField("zone", StringType(), True),
    StructField("count", LongType(), True) # L'agrégation count() retourne un Long
])

# ======================================
# 2. READ STREAMING (Supprimez l'étape spark.read.json)
# ======================================

traffic_zone_stream = (
    spark.readStream
    .schema(traffic_zone_schema)
    .json("hdfs://namenode:8020/data/processed/traffic/traffic_zone")
)

speed_route_stream = (
    spark.readStream
    .schema(speed_route_schema)
    .json("hdfs://namenode:8020/data/processed/traffic/speed_route")
)

congestion_stream = (
    spark.readStream
    .schema(congestion_schema)
    .json("hdfs://namenode:8020/data/processed/traffic/congestion")
)

# ======================================
# 3. Spark Session
# ======================================
spark = (
    SparkSession.builder
    .appName("TrafficAnalyticsZoneStreaming")
    .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:8020")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

# ======================================
# 4. READ SCHEMA (BATCH MODE)
# ======================================

traffic_zone_schema = (
    spark.read
    .json("hdfs://namenode:8020/data/processed/traffic/traffic_zone")
    .schema
)

speed_route_schema = (
    spark.read
    .json("hdfs://namenode:8020/data/processed/traffic/speed_route")
    .schema
)

congestion_schema = (
    spark.read
    .json("hdfs://namenode:8020/data/processed/traffic/congestion")
    .schema
)

# ======================================
# 5. READ STREAMING WITH SCHEMA
# ======================================

traffic_zone_stream = (
    spark.readStream
    .schema(traffic_zone_schema)
    .json("hdfs://namenode:8020/data/processed/traffic/traffic_zone")
)

speed_route_stream = (
    spark.readStream
    .schema(speed_route_schema)
    .json("hdfs://namenode:8020/data/processed/traffic/speed_route")
)

congestion_stream = (
    spark.readStream
    .schema(congestion_schema)
    .json("hdfs://namenode:8020/data/processed/traffic/congestion")
)

# ======================================
# 6. ANALYTICS STRUCTURATION (KPI)
# ======================================

traffic_zone_analytics = traffic_zone_stream.select(
    col("zone"),
    col("window.start").alias("window_start"),
    col("window.end").alias("window_end"),
    col("avg_vehicle_count")
)

speed_route_analytics = speed_route_stream.select(
    col("road_id"),
    col("window.start").alias("window_start"),
    col("window.end").alias("window_end"),
    col("avg_speed")
)

congestion_analytics = congestion_stream.select(
    col("zone"),
    col("window.start").alias("window_start"),
    col("window.end").alias("window_end"),
    col("count").alias("congestion_events")
)

# ======================================
# 5. WRITE STREAMING → ANALYTICS ZONE
# ======================================

traffic_zone_query = (
    traffic_zone_analytics.writeStream
    .outputMode("append")
    .format("parquet")
    .option(
        "path",
        "hdfs://namenode:8020/data/analytics/traffic/traffic_by_zone"
    )
    .option(
        "checkpointLocation",
        "hdfs://namenode:8020/checkpoints/analytics/traffic_by_zone"
    )
    .start()
)

speed_route_query = (
    speed_route_analytics.writeStream
    .outputMode("append")
    .format("parquet")
    .option(
        "path",
        "hdfs://namenode:8020/data/analytics/traffic/speed_by_road"
    )
    .option(
        "checkpointLocation",
        "hdfs://namenode:8020/checkpoints/analytics/speed_by_road"
    )
    .start()
)

congestion_query = (
    congestion_analytics.writeStream
    .outputMode("append")
    .format("parquet")
    .option(
        "path",
        "hdfs://namenode:8020/data/analytics/traffic/congestion_by_zone"
    )
    .option(
        "checkpointLocation",
        "hdfs://namenode:8020/checkpoints/analytics/congestion_by_zone"
    )
    .start()
)

# ======================================
# 6. Await termination
# ======================================
spark.streams.awaitAnyTermination()
