import json
import uuid
import time
import random
from kafka import KafkaProducer
from threading import Thread



producer = KafkaProducer( bootstrap_servers= "localhost:9092",
                          value_serializer= lambda v: json.dumps(v).encode("utf-8"),
                          key_serializer= lambda k: k.encode("utf-8")
)


STATUSES = ['created','matched','picked_up','delivered']
CITY_CENTERS = (37.77,-122.4149)


def random_point():

    return ( 
        CITY_CENTERS[0] + random.uniform(-0.005, 0.005),
        CITY_CENTERS[1] + random.uniform(-0.005, 0.005)
    )


print("Simulating Orders")

while True: 

    order_id = str(uuid.uuid4())[:8]
    lat, lon = random_point()


    for status in STATUSES:
        event = { 
            "order_id": order_id,
            "status": status,
            "lat": round(lat, 6),
            "lon": round(lon, 6),
            "driver_id": f'driver-{random.randint(0,14)}' if status != 'created' else None,
            "timestamp": time.time()
        }

       #print(f'{event} \t {status}')
        producer.send("order-events", key="order_id", value = event)
        producer.flush()
        time.sleep(random.uniform(2,5))

    time.sleep(random.uniform(1,3))







    






