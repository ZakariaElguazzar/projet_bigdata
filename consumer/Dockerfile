FROM python:3.11-slim

# Éviter les buffers (logs immédiats)
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Code
COPY kafka_to_hdfs.py .

# Lancement
CMD ["python", "kafka_to_hdfs.py"]
