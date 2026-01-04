import random
from datetime import datetime

sensors = ['S1', 'S2', 'S3', 'S4', 'S5']
roads = ['R1', 'R2', 'R3']
road_types = ['autoroute', 'avenue', 'rue']
zones = ['Nord', 'Sud', 'Est', 'Ouest']

def generate_event():
    sensor_id = random.choice(sensors)
    road_id = random.choice(roads)
    road_type = random.choice(road_types)
    zone = random.choice(zones)
    
    hour = datetime.now().hour
    if 7 <= hour <= 9 or 17 <= hour <= 19:  # heures de pointe
        vehicle_count = random.randint(20, 100)
        average_speed = random.randint(20, 50)
        occupancy_rate = random.randint(50, 90)
    else:
        vehicle_count = random.randint(5, 30)
        average_speed = random.randint(40, 80)
        occupancy_rate = random.randint(10, 50)

    return {
        "sensor_id": sensor_id,
        "road_id": road_id,
        "road_type": road_type,
        "zone": zone,
        "vehicle_count": vehicle_count,
        "average_speed": average_speed,
        "occupancy_rate": occupancy_rate,
        "event_time": datetime.now().isoformat()
    }
