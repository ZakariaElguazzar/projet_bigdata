from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, window
from pyspark.sql.types import (
    StructType, StructField,
    StringType, IntegerType,
    DoubleType, TimestampType
)

# ======================================
# 1. Spark Session
# ======================================
spark = (
    SparkSession.builder
    .appName("TrafficEndToEndAnalytics")
    .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:8020")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

# ======================================
# 2. Schema RAW
# ======================================
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

# ======================================
# 3. Read RAW stream from HDFS
# ======================================
df = (
    spark.readStream
    .schema(schema)
    .json("hdfs://namenode:8020/data/raw/traffic/")
)

# ======================================
# 4. WINDOWED AGGREGATIONS
# ======================================

# ---- Traffic by zone
traffic_zone = (
    df.withWatermark("event_time", "2 minutes")
      .groupBy(
          window(col("event_time"), "2 minutes"),
          col("zone")
      )
      .agg(avg("vehicle_count").alias("avg_vehicle_count"))
      .select(
          col("zone"),
          col("window.start").alias("window_start"),
          col("window.end").alias("window_end"),
          col("avg_vehicle_count")
      )
)

# ---- Speed by road
speed_route = (
    df.withWatermark("event_time", "2 minutes")
      .groupBy(
          window(col("event_time"), "2 minutes"),
          col("road_id")
      )
      .agg(avg("average_speed").alias("avg_speed"))
      .select(
          col("road_id"),
          col("window.start").alias("window_start"),
          col("window.end").alias("window_end"),
          col("avg_speed")
      )
)

# ---- Congestion by zone
congestion = (
    df.filter(col("occupancy_rate") > 70)
      .withWatermark("event_time", "2 minutes")
      .groupBy(
          window(col("event_time"), "2 minutes"),
          col("zone")
      )
      .count()
      .select(
          col("zone"),
          col("window.start").alias("window_start"),
          col("window.end").alias("window_end"),
          col("count").alias("congestion_events")
      )
)

# ======================================
# 5. WRITE ANALYTICS (FINAL)
# ======================================

traffic_zone_query = (
    traffic_zone.writeStream
    .outputMode("append")
    .format("json")
    .option(
        "path",
        "hdfs://namenode:8020/data/analytics/traffic/traffic_by_zone"
    )
    .option(
        "checkpointLocation",
        "hdfs://namenode:8020/checkpoints/analytics/traffic_by_zone"
    )
    .trigger(processingTime="1 minute")
    .start()
)

speed_route_query = (
    speed_route.writeStream
    .outputMode("append")
    .format("json")
    .option(
        "path",
        "hdfs://namenode:8020/data/analytics/traffic/speed_by_road"
    )
    .option(
        "checkpointLocation",
        "hdfs://namenode:8020/checkpoints/analytics/speed_by_road"
    )
    .trigger(processingTime="1 minute")
    .start()
)

congestion_query = (
    congestion.writeStream
    .outputMode("append")
    .format("json")
    .option(
        "path",
        "hdfs://namenode:8020/data/analytics/traffic/congestion_by_zone"
    )
    .option(
        "checkpointLocation",
        "hdfs://namenode:8020/checkpoints/analytics/congestion_by_zone"
    )
    .trigger(processingTime="1 minute")
    .start()
)

# ======================================
# 6. Await termination
# ======================================
spark.streams.awaitAnyTermination()
