# Smart City Traffic Analytics Pipeline

A comprehensive end-to-end Big Data pipeline for real-time urban traffic analysis and intelligent mobility management, built with modern data engineering technologies.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Technologies](#technologies)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Data Flow](#data-flow)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🌟 Overview

This project implements a complete Big Data pipeline designed for Smart City traffic monitoring and analysis. The system collects real-time traffic data from simulated urban sensors, processes it through a streaming architecture, and provides actionable insights through interactive dashboards.

### Business Context

Modern cities deploy various sensors (cameras, magnetic loops, IoT devices, mobile applications) to continuously collect traffic-related data. This pipeline enables municipalities to:

- **Monitor** real-time traffic conditions
- **Detect** congestion zones
- **Analyze** vehicle flows by zone, period, and road type
- **Improve** urban planning and mobility management
- **Support** data-driven decision making

### Key Features

- ✅ Real-time data ingestion using Apache Kafka
- ✅ Scalable storage with HDFS Data Lake
- ✅ Stream processing with Apache Spark
- ✅ Automated orchestration via Apache Airflow
- ✅ Comprehensive monitoring with Prometheus & Grafana
- ✅ Multi-zone analytics and KPI generation
- ✅ Fully containerized deployment with Docker

## 🏗️ Architecture

The pipeline follows a Lambda Architecture pattern with the following layers:

```
┌─────────────────┐
│  Data Sources   │ → Simulated Traffic Sensors
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Kafka Producer  │ → Real-time event generation
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Apache Kafka   │ → Message queue (traffic-events topic)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Kafka Consumer  │ → HDFS writer
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  HDFS Raw Zone  │ → /data/raw/traffic/
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Spark Stream   │ → Real-time processing
│   Processing    │
└────────┬────────┘
         │
         ├─→ /data/processed/traffic/traffic_zone
         ├─→ /data/processed/traffic/speed_route
         └─→ /data/processed/traffic/congestion
         │
         ▼
┌─────────────────┐
│ Spark Analytics │ → KPI computation
└────────┬────────┘
         │
         ├─→ /data/analytics/traffic/traffic_by_zone
         ├─→ /data/analytics/traffic/speed_by_road
         └─→ /data/analytics/traffic/congestion_by_zone
         │
         ▼
┌─────────────────┐
│ HDFS Exporter   │ → Metrics extraction
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Prometheus     │ → Metrics storage
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Grafana      │ → Visualization & Dashboards
└─────────────────┘

        ⬆
        │
┌─────────────────┐
│ Apache Airflow  │ → Pipeline orchestration
└─────────────────┘
```

## 🛠️ Technologies

### Core Components

| Technology | Version | Purpose |
|------------|---------|---------|
| **Apache Kafka** | 6.2.1 | Real-time data ingestion and streaming |
| **Apache Zookeeper** | 6.2.1 | Kafka cluster coordination |
| **Apache Hadoop (HDFS)** | 3.3.6 | Distributed data lake storage |
| **Apache Spark** | Latest | Stream processing and analytics |
| **Apache Airflow** | 2.8.1 | Workflow orchestration and scheduling |
| **Prometheus** | Latest | Metrics collection and monitoring |
| **Grafana** | Latest | Data visualization and dashboards |
| **PostgreSQL** | 13 | Airflow metadata database |
| **Docker** | - | Containerization platform |

### Programming Languages & Libraries

- **Python 3.x**
  - `kafka-python`: Kafka producer/consumer
  - `pyspark`: Spark streaming and analytics
  - `hdfs`: HDFS client
  - `prometheus_client`: Metrics exporter

## 📁 Project Structure

```
smart-city-traffic-pipeline/
│
├── docker-compose.yml              # Multi-container orchestration
├── config                          # Hadoop configuration files
│
├── producer/
│   ├── Dockerfile
│   ├── kafka_producer.py          # Kafka event producer
│   ├── traffic_generator.py       # Traffic data simulator
│   └── requirements.txt
│
├── consumer/
│   ├── Dockerfile
│   ├── kafka_to_hdfs.py          # Kafka → HDFS consumer
│   └── requirements.txt
│
├── spark/
│   ├── data_traitement.py        # Spark streaming processing
│   ├── traffic_analytics.py      # Analytics computation
│   └── start-spark-jobs.sh       # Spark job launcher
│
├── exporter/
│   ├── Dockerfile
│   ├── hdfs_exporter.py          # HDFS → Prometheus exporter
│   └── requirements.txt
│
├── monitoring/
│   ├── prometheus/
│   │   └── prometheus.yml        # Prometheus configuration
│   └── jmx/
│       ├── jmx_prometheus_javaagent-0.20.0.jar
│       └── hadoop.yml            # JMX exporter config
│
├── airflow/
│   ├── dags/
│   │   └── bigdata_pipeline.py   # Airflow DAG definition
│   ├── logs/
│   └── plugins/
│
└── hdfs-init.sh                   # HDFS initialization script
```

## 📊 Data Model

### Traffic Event Schema

Each traffic event contains the following fields:

```json
{
  "sensor_id": "S1",
  "road_id": "R1",
  "road_type": "autoroute",
  "zone": "Nord",
  "vehicle_count": 45,
  "average_speed": 65.5,
  "occupancy_rate": 75.2,
  "event_time": "2026-01-14T10:30:00.000000"
}
```

**Field Descriptions:**

- `sensor_id`: Unique identifier for the traffic sensor
- `road_id`: Road segment identifier
- `road_type`: Type of road (autoroute, avenue, rue)
- `zone`: Geographic zone (Nord, Sud, Est, Ouest)
- `vehicle_count`: Number of vehicles detected in the measurement window
- `average_speed`: Average vehicle speed in km/h
- `occupancy_rate`: Road occupancy percentage (0-100)
- `event_time`: ISO 8601 timestamp of the measurement

### Analytics Outputs

#### 1. Traffic by Zone
```json
{
  "zone": "Nord",
  "window_start": "2026-01-14T10:00:00.000Z",
  "window_end": "2026-01-14T10:02:00.000Z",
  "avg_vehicle_count": 42.5
}
```

#### 2. Speed by Road
```json
{
  "road_id": "R1",
  "window_start": "2026-01-14T10:00:00.000Z",
  "window_end": "2026-01-14T10:02:00.000Z",
  "avg_speed": 58.3
}
```

#### 3. Congestion by Zone
```json
{
  "zone": "Est",
  "window_start": "2026-01-14T10:00:00.000Z",
  "window_end": "2026-01-14T10:02:00.000Z",
  "congestion_events": 15
}
```

## 🚀 Prerequisites

### System Requirements

- **Docker**: Version 20.10 or higher
- **Docker Compose**: Version 2.0 or higher
- **RAM**: Minimum 8GB (16GB recommended)
- **Storage**: At least 20GB free space
- **CPU**: Multi-core processor recommended

### Network Ports

Ensure the following ports are available:

| Port | Service | Description |
|------|---------|-------------|
| 2181 | Zookeeper | Coordination service |
| 9092 | Kafka | Message broker |
| 9870 | HDFS NameNode | Web UI |
| 8020 | HDFS NameNode | RPC |
| 9864 | HDFS DataNode | Web UI |
| 7077 | Spark Master | Cluster manager |
| 8080 | Spark Master | Web UI |
| 8000 | HDFS Exporter | Prometheus metrics |
| 9090 | Prometheus | Metrics server |
| 3000 | Grafana | Dashboards |
| 8085 | Airflow | Web UI |
| 5432 | PostgreSQL | Airflow database |

## 📦 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/smart-city-traffic-pipeline.git
cd smart-city-traffic-pipeline
```

### Step 2: Create Required Directories

```bash
mkdir -p airflow/dags airflow/logs airflow/plugins
mkdir -p monitoring/prometheus monitoring/jmx
chmod -R 755 airflow/
```

### Step 3: Build Docker Images

```bash
docker-compose build
```

This will build custom images for:
- Kafka Producer
- Kafka Consumer
- HDFS Exporter
- Spark (with custom applications)

### Step 4: Start the Infrastructure

```bash
docker-compose up -d
```

### Step 5: Verify Services

Check that all containers are running:

```bash
docker-compose ps
```

Expected output should show all services as "Up".

## ⚙️ Configuration

### Hadoop Configuration

Edit the `config` file to adjust HDFS settings:

```properties
fs.defaultFS=hdfs://namenode:8020
dfs.replication=1
dfs.namenode.name.dir=file:///tmp/hadoop-root/dfs/name
dfs.datanode.data.dir=file:///tmp/hadoop-root/dfs/data
```

### Kafka Configuration

Modify `docker-compose.yml` to adjust Kafka settings:

```yaml
KAFKA_AUTO_CREATE_TOPICS_ENABLE: "true"
KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
```

### Spark Configuration

Adjust Spark streaming parameters in `data_traitement.py`:

```python
# Window duration for aggregations
.groupBy(window(col("event_time"), "2 minutes"), col("zone"))

# Watermark for late data handling
.withWatermark("event_time", "2 minutes")

# Processing trigger interval
.trigger(processingTime="1 minute")
```

### Prometheus Configuration

Edit `monitoring/prometheus/prometheus.yml`:

```yaml
scrape_configs:
  - job_name: 'hdfs-exporter'
    static_configs:
      - targets: ['hdfs-exporter:8000']
    scrape_interval: 10s
```

## 🎯 Usage

### Manual Pipeline Execution

#### 1. Start Data Generation

The Kafka producer automatically starts and generates traffic events continuously:

```bash
docker logs -f kafka-producer
```

Expected output:
```
Kafka connected
Sending events...
```

#### 2. Verify Kafka Ingestion

Check that messages are being produced:

```bash
docker exec -it kafka kafka-console-consumer \
  --bootstrap-server kafka:9092 \
  --topic traffic-events \
  --from-beginning --max-messages 5
```

#### 3. Monitor HDFS Storage

Verify raw data is being written:

```bash
docker exec -it namenode hdfs dfs -ls /data/raw/traffic/
```

#### 4. Check Spark Processing

View Spark streaming job status:

```bash
# Spark Master UI
http://localhost:8080

# View Spark logs
docker logs -f spark-master
```

#### 5. Verify Analytics Output

Check processed analytics:

```bash
docker exec -it namenode hdfs dfs -ls /data/analytics/traffic/traffic_by_zone/
docker exec -it namenode hdfs dfs -cat /data/analytics/traffic/traffic_by_zone/*.json | head -5
```

### Automated Pipeline with Airflow

#### 1. Access Airflow UI

Navigate to: `http://localhost:8085`

**Credentials:**
- Username: `admin`
- Password: `admin`

#### 2. Trigger the DAG

1. Locate the `traffic_pipeline_orchestration` DAG
2. Toggle it ON
3. Click "Trigger DAG" button
4. Monitor execution in the Graph View

The DAG will execute the following tasks in order:
1. Start Kafka Producer
2. Wait for data generation
3. Start Kafka Consumer
4. Start Spark Master
5. Start Spark Worker
6. Start HDFS Exporter
7. Start Prometheus
8. Start Grafana

## 📈 Monitoring

### Prometheus Metrics

Access Prometheus at: `http://localhost:9090`

**Available Metrics:**

- `traffic_vehicle_count{zone="Nord"}`: Average vehicle count by zone
- `traffic_road_speed{road_id="R1"}`: Average speed by road
- `traffic_congestion_events{zone="Est"}`: Congestion event count by zone

**Example Queries:**

```promql
# Average traffic across all zones
avg(traffic_vehicle_count)

# Roads with speed below 30 km/h
traffic_road_speed < 30

# Total congestion events
sum(traffic_congestion_events)
```

### Grafana Dashboards

Access Grafana at: `http://localhost:3000`

**Credentials:**
- Username: `admin`
- Password: `admin`

#### Creating a Dashboard

1. Add Prometheus as a data source:
   - Configuration → Data Sources → Add Prometheus
   - URL: `http://prometheus:9090`

2. Create a new dashboard with panels:

**Panel 1: Traffic by Zone**
```promql
traffic_vehicle_count
```
- Visualization: Time series
- Legend: {{zone}}

**Panel 2: Average Speed Heatmap**
```promql
traffic_road_speed
```
- Visualization: Heatmap
- Legend: {{road_id}}

**Panel 3: Congestion Alerts**
```promql
traffic_congestion_events > 10
```
- Visualization: Stat
- Thresholds: 10 (warning), 20 (critical)

**Panel 4: Real-time Traffic Status**
```promql
sum by (zone) (traffic_vehicle_count)
```
- Visualization: Gauge

### HDFS Monitoring

**NameNode Web UI:** `http://localhost:9870`

Key metrics to monitor:
- Cluster capacity and usage
- Live/dead nodes
- File system health
- Block statistics

**DataNode Web UI:** `http://localhost:9864`

### Spark Monitoring

**Spark Master Web UI:** `http://localhost:8080`

Monitor:
- Running applications
- Worker nodes status
- Completed jobs
- Resource utilization

**Spark Application UI:** Available through the Master UI

Track:
- Streaming queries
- Processing rates
- Batch durations
- Data sources and sinks

## 🔍 Data Flow Deep Dive

### Stage 1: Data Generation

The `traffic_generator.py` simulates realistic traffic patterns:

```python
# Peak hours (7-9 AM, 5-7 PM)
vehicle_count: 20-100
average_speed: 20-50 km/h
occupancy_rate: 50-90%

# Off-peak hours
vehicle_count: 5-30
average_speed: 40-80 km/h
occupancy_rate: 10-50%
```

### Stage 2: Kafka Ingestion

Events are published to the `traffic-events` topic with:
- Automatic partitioning
- JSON serialization
- Retry logic for fault tolerance

### Stage 3: HDFS Raw Storage

Consumer writes to HDFS with:
- Timestamped file naming: `{timestamp}.json`
- Automatic directory creation
- Append-only writes for immutability

### Stage 4: Spark Stream Processing

**data_traitement.py** performs:

1. **Windowed Aggregations** (2-minute windows)
   - Traffic by zone
   - Speed by road
   - Congestion detection (occupancy > 70%)

2. **Watermarking** for late data handling

3. **Checkpointing** for fault recovery

### Stage 5: Analytics Computation

**traffic_analytics.py** restructures processed data:

- Flattens nested window structures
- Renames fields for clarity
- Prepares data for metrics export

### Stage 6: Metrics Export

**hdfs_exporter.py**:
- Reads latest analytics files
- Updates Prometheus gauges
- Handles JSON Lines format
- 10-second refresh interval

## 🛠️ Troubleshooting

### Common Issues

#### 1. Kafka Connection Errors

**Symptom:** Producer/Consumer can't connect to Kafka

**Solution:**
```bash
# Check Kafka is running
docker logs kafka

# Verify Zookeeper is healthy
docker logs zookeeper

# Restart Kafka
docker-compose restart kafka
```

#### 2. HDFS NameNode Not Starting

**Symptom:** NameNode container exits immediately

**Solution:**
```bash
# Format NameNode (WARNING: deletes all data)
docker exec -it namenode hdfs namenode -format

# Restart NameNode
docker-compose restart namenode
```

#### 3. Spark Jobs Not Starting

**Symptom:** No streaming queries appear in Spark UI

**Solution:**
```bash
# Check Spark Master logs
docker logs spark-master

# Verify HDFS connectivity
docker exec -it spark-master hdfs dfs -ls /

# Restart Spark services
docker-compose restart spark-master spark-worker-1
```

#### 4. No Data in Grafana

**Symptom:** Grafana panels show "No data"

**Solution:**
```bash
# Verify HDFS exporter is running
docker logs hdfs-exporter

# Check Prometheus is scraping
curl http://localhost:9090/api/v1/targets

# Verify analytics files exist
docker exec -it namenode hdfs dfs -ls /data/analytics/traffic/
```

#### 5. Airflow DAG Not Appearing

**Symptom:** DAG doesn't show in Airflow UI

**Solution:**
```bash
# Check DAG file is in correct location
ls -la airflow/dags/

# Verify Airflow scheduler is running
docker logs airflow-scheduler

# Refresh DAG
docker exec -it airflow-webserver airflow dags list
```

### Performance Tuning

#### Increase Spark Processing Speed

Edit `data_traitement.py`:
```python
# Reduce trigger interval
.trigger(processingTime="30 seconds")

# Increase parallelism
spark.conf.set("spark.sql.shuffle.partitions", "10")
```

#### Optimize Kafka Throughput

Edit `docker-compose.yml`:
```yaml
KAFKA_NUM_PARTITIONS: 3
KAFKA_DEFAULT_REPLICATION_FACTOR: 1
```

#### Scale HDFS Storage

Add more DataNodes in `docker-compose.yml`:
```yaml
datanode-2:
  image: apache/hadoop:3.3.6
  container_name: datanode-2
  # ... similar config
```

### Logs and Debugging

View logs for specific services:

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f kafka-producer

# Last 100 lines
docker-compose logs --tail=100 spark-master

# Follow new logs only
docker-compose logs -f --since 5m
```

## 🧪 Testing

### Unit Testing

Test the traffic generator:

```bash
cd producer
python3 -c "from traffic_generator import generate_event; print(generate_event())"
```

### Integration Testing

Verify end-to-end flow:

```bash
# 1. Generate and send one event
docker exec -it kafka-producer python3 -c "
from traffic_generator import generate_event
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
event = generate_event()
producer.send('traffic-events', value=event)
print(f'Sent: {event}')
"

# 2. Verify in HDFS (wait 10 seconds)
sleep 10
docker exec -it namenode hdfs dfs -cat /data/raw/traffic/*.json | tail -1

# 3. Check processed output (wait 2 minutes for window)
sleep 120
docker exec -it namenode hdfs dfs -cat /data/processed/traffic/traffic_zone/*.json | tail -1
```

### Load Testing

Generate high-volume traffic:

```python
# Modify kafka_producer.py
while True:
    for _ in range(100):  # Send 100 events per iteration
        event = generate_event()
        producer.send('traffic-events', value=event)
    producer.flush()
    time.sleep(1)  # Adjust for desired throughput
```

## 🔒 Security Considerations

### Current Setup (Development)

⚠️ **This setup is for development/testing only**

- No authentication on Kafka
- HDFS runs in insecure mode
- Default credentials for services
- No encryption in transit

### Production Recommendations

1. **Enable Kafka Security:**
   - SSL/TLS encryption
   - SASL authentication
   - ACLs for topic access

2. **Secure HDFS:**
   - Kerberos authentication
   - Encryption at rest and in transit
   - User permissions and quotas

3. **Airflow Security:**
   - Change default passwords
   - Enable RBAC
   - Use secrets backend (e.g., Vault)

4. **Network Security:**
   - Use Docker networks
   - Firewall rules
   - VPN for remote access

## 📚 Additional Resources

### Documentation

- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Apache Spark Structured Streaming](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html)
- [Apache Hadoop HDFS](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsUserGuide.html)
- [Apache Airflow](https://airflow.apache.org/docs/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Tutorials](https://grafana.com/tutorials/)

### Related Projects

- [Confluent Platform](https://docs.confluent.io/)
- [Databricks](https://databricks.com/)
- [Cloudera Data Platform](https://www.cloudera.com/)

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to branch: `git push origin feature/new-feature`
5. Submit a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Add docstrings to functions
- Update documentation for new features
- Test changes locally before submitting

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- **Zakaria El Guazzar** - *ZakariaElguazzar* - [Your GitHub](https://github.com/ZakariaElguazzar)

## 🙏 Acknowledgments

- Smart City initiatives worldwide
- Apache Software Foundation projects
- Open-source community contributors
- Data engineering best practices from the community

---

**Project Status:** ✅ Active Development

**Last Updated:** January 2026

For questions or support, please open an issue on GitHub.
