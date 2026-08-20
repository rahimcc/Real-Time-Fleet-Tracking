import json
import random
import time 
from kafka import KafkaProducer
from kafka.errors import KafkaError
import socket
import logging



logging.basicConfig(level=logging.DEBUG)

host = "localhost"
port = 9092


try: 
    sock = socket.create_connection((host,port), timeout = 5 )
    print(f" TCP connection to {host}:{port} succeded ")
    sock.close()

except Exception as e:

    print(f'TCP connection failed')




BOOTSTRAP = "127.0.0.1:9092"
CITY_CENTER = (37.7749, -122.4194)
NUM_DRIVERS = 15


try:
    producer = KafkaProducer( 
          bootstrap_servers=BOOTSTRAP,
          value_serializer=lambda v: json.dumps(v).encode('utf-8'),
          key_serializer=lambda k: k.encode('utf-8')
    )
    print("Bootstrap connected: ", producer.bootstrap_connected())

except KafkaError as e:
     print(f"Connection failed {e}")


drivers = { 
    f'driver-{i}': { 
        "lat": CITY_CENTER[0] + random.uniform(-0.05, 0.05),
        "lon": CITY_CENTER[1] + random.uniform(-0.05,0.05),
        "status": "available"
        } for i in range(NUM_DRIVERS)
    }

print(f'Simulating {NUM_DRIVERS} drivers... Ctrl + C to Stop')


while True: 
    for driver_id, state in drivers.items():

        state['lat'] += random.uniform(-0.001, 0.001)
        state['lon'] += random.uniform(-0.001, 0.001)

        event = { 
            "driver_id": driver_id,
            "lat": round(state['lat'],6),
            "lon": round(state['lon'],6),
            "speed_kmh": round(random.uniform(0,60),1),
            "status": state['status'],
            "timestamp": time.time() 
        }


        producer.send('driver-locations', key=driver_id, value=event)

    producer.flush()
    time.sleep(1.5)

