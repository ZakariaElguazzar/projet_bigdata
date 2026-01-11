import time
import json
import os
from hdfs import InsecureClient
from prometheus_client import start_http_server, Gauge

# ==========================================
# CONFIGURATION
# ==========================================
HDFS_URL = 'http://namenode:9870'
HDFS_USER = 'hadoop'
UPDATE_INTERVAL = 10  # secondes

# ==========================================
# DÉFINITION DES MÉTRIQUES PROMETHEUS
# ==========================================
# Gauge = indicateur qui peut monter/descendre (ex: vitesse, compte)
TRAFFIC_COUNT = Gauge('traffic_vehicle_count', 'Nombre moyen de véhicules', ['zone'])
ROAD_SPEED = Gauge('traffic_road_speed', 'Vitesse moyenne sur la route', ['road_id'])
CONGESTION_EVENTS = Gauge('traffic_congestion_events', 'Nombre d\'événements de congestion', ['zone'])

def get_latest_file_content(client, directory):
    """
    Récupère le contenu du fichier le plus récent dans un dossier HDFS.
    CORRECTION : Gestion correcte du format de retour de client.list()
    """
    try:
        # status=True fait que client.list retourne une liste de tuples :
        # [(nom_fichier_1, {metadata_1}), (nom_fichier_2, {metadata_2})]
        files_with_status = client.list(directory, status=True)
        
        candidates = []
        for filename, metadata in files_with_status:
            # On filtre : on veut des FICHIERS (pas des dossiers) et du JSON
            if metadata['type'] == 'FILE' and filename.endswith('.json'):
                # On ajoute le nom dans les métadonnées pour l'utiliser après
                metadata['_name'] = filename
                candidates.append(metadata)
        
        if not candidates:
            return []

        # Trie par date de modification ('modificationTime') pour prendre le dernier
        candidates.sort(key=lambda x: x['modificationTime'])
        latest_file_meta = candidates[-1]
        
        full_path = os.path.join(directory, latest_file_meta['_name'])
        # print(f"Lecture du fichier : {full_path}") # Décommentez pour debug
        
        # Lecture du contenu
        with client.read(full_path) as reader:
            content = reader.read().decode('utf-8')
            # Spark Streaming écrit souvent en "JSON Lines" (un objet JSON par ligne)
            records = []
            for line in content.strip().split('\n'):
                if line.strip():
                    try:
                        records.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
            return records

    except Exception as e:
        # On affiche l'erreur mais on ne crash pas le script
        # C'est normal d'avoir "File does not exist" au tout début, tant que Spark n'a rien écrit
        print(f"Info/Erreur lecture HDFS {directory}: {e}")
        return []

def update_metrics(client):
    print("Mise à jour des métriques...")
    
    # --- 1. Traitement Traffic Zone ---
    zones_data = get_latest_file_content(client, '/data/analytics/traffic/traffic_by_zone')
    for record in zones_data:
        # On vérifie que les clés existent bien dans le JSON
        if 'zone' in record and 'avg_vehicle_count' in record:
            TRAFFIC_COUNT.labels(zone=record['zone']).set(record['avg_vehicle_count'])

    # --- 2. Traitement Speed Route ---
    speed_data = get_latest_file_content(client, '/data/analytics/traffic/speed_by_road')
    for record in speed_data:
        if 'road_id' in record and 'avg_speed' in record:
            ROAD_SPEED.labels(road_id=record['road_id']).set(record['avg_speed'])
    
    congestion_data = get_latest_file_content(client, '/data/analytics/traffic/congestion_by_zone')
    for record in congestion_data:
        if 'zone' in record and 'congestion_events' in record:
            CONGESTION_EVENTS.labels(zone=record['zone']).set(record['congestion_events'])

if __name__ == '__main__':
    # Démarre le serveur web pour que Prometheus puisse venir lire les données
    start_http_server(8000)
    print("Exporter HDFS démarré sur le port 8000")
    
    # Connexion au Namenode
    client = InsecureClient(HDFS_URL, user=HDFS_USER)
    
    # Boucle infinie
    while True:
        update_metrics(client)
        time.sleep(UPDATE_INTERVAL)