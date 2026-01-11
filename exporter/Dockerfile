FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Code
COPY hdfs_exporter.py .

# Port Prometheus
EXPOSE 8000

# Lancement
CMD ["python", "hdfs_exporter.py"]
