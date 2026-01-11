#!/bin/bash
# start-spark-jobs.sh
set -e

echo "Starting Spark Master..."
/opt/spark/bin/spark-class org.apache.spark.deploy.master.Master \
  --host spark-master --port 7077 --webui-port 8080 &

# Attendre que le master soit prêt
echo "Waiting for Spark Master to be ready..."
sleep 10  # ajuste si besoin

# Chemin vers tes scripts
SPARK_APPS_DIR=/opt/spark/apps

# 1️⃣ Lancer traffic_pipeline_analytics.py
echo "Submitting traffic_pipeline_analytics.py..."
/opt/spark/bin/spark-submit $SPARK_APPS_DIR/traffic_pipeline_analytics.py 


# Garder le container actif
tail -f /dev/null
