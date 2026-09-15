import json
import time 
import random
from kafka import KafkaProducer
from kafka.errors import KafkaError
import socket
import logging
from backend.static.constants import BOOTSTRAP, CITY_CENTER , NUM_DRIVERS
from backend.static.baku_metro_stations import BAKU_METRO_STATIONS
from backend.services.routing import pick_random_trip, fetch_route
import asyncio


ECONDS_PER_HOUR = 3600
KM_PER_DEGREE_LATITUDE = 111

host = "localhost"
port = 9092


class Vehicle:

    def __init__(self, vehicle_id):
        self.vehicle_id = vehicle_id
        self.lat = 0
        self.lon = 0
        self.speed_kmh = 0
        self.heading = 0
        self.route = []
        self.route_index = 0
        self.trip_label = ""
        self.start_name = ""
        self.end_name = ""
        self.start_coord = ()
        self.end_coord = ()

    def start_new_trip(self) -> None:

        self.start_name, self.end_name = pick_random_trip() # Pick two random Metro Station name   
        # Convert station name to coordinates
        self.start_coord = BAKU_METRO_STATIONS[self.start_name] 
        self.end_coord = BAKU_METRO_STATIONS[self.end_name]

        # Fetch route between these two coordinates
        new_route = fetch_route(self.start_coord[0],self.start_coord[1]\
                                ,self.end_coord[0], self.end_coord[1])
        
        if new_route: 
           self.route = new_route 
           self.route_index = 0
           print(f'New trip: {self.start_name} -> {self.end_name} ({len(self.route)} points)')
           #print(route)
        else: 
            print(f'Failed to fetch route from {self.start_name} to {self.end_name}, retrying next tick')



    async def simulate_vehicle(self, broadcast) -> None:
        """Moves the vehicle a small random step every second"""

        print("Hello")
        self.start_new_trip()
        producer = KafkaProducer( 
                                bootstrap_servers="kafka:9092",
                                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                                key_serializer=lambda k: k.encode("utf-8")
                            )

        while True:
            try:
                if not self.route:
                    print(f'Not route: {self.route}')
                    self.start_new_trip()
                    await asyncio.sleep(1)


                if self.route_index >= len(self.route):

                    print(f'Route index bigger.')
                    print(f'Route len= {len(self.route)}')
                    print(f'Route index = {self.route_index}')
                    self.start_new_trip()
                    await asyncio.sleep(1)
                    continue


                self.lon, self.lat = self.route[self.route_index]


                self.route_index += 1
                print('Route index icremented')

                payload = {
                    "vehicle-id": self.vehicle_id,
                    "lat": round(self.lat,6),
                    "lon": round(self.lon,6),
                    "heading": self.heading,
                    "trip":  f'{self.start_name} -> {self.end_name}',
                    "start_lat": self.start_coord[0], "start_lon": self.start_coord[1],
                    "end_lat": self.end_coord[0], "end_lon": self.end_coord[1],
                    "timestamp": time.time(),
                    "test": "test"
                }

               # print(payload)
              
                
                
                producer.send("vehicle-locations", key=self.vehicle_id, value=payload)
                producer.flush()
                print("Event sent to Kafka")

                await broadcast(payload)
                await asyncio.sleep(1)

            except Exception as e:
                print(f'simulate_vehicle loop error: {e}')
                break
                
        await asyncio.sleep(1)

#logging.basicConfig(level=logging.DEBUG)

def test_kafka(host,port) -> bool:
    """
    - Connects to Kafka to check connection
    
    Args: host, port

    Returns: Boolean value 
    """
    try: 
        sock = socket.create_connection((host,port), timeout = 5)
        print(f"TCP connection to {host}:{port} succeded.")
        sock.close()
        return True

    except Exception as e:
        print(f'TCP connection failed')
        return False
"""
try:
    producer = KafkaProducer( 
          bootstrap_servers=BOOTSTRAP ,
          value_serializer=lambda v: json.dumps(v).encode('utf-8'),
          key_serializer=lambda k: k.encode('utf-8')
    )
    print("Bootstrap connected: ", producer.bootstrap_connected())

except KafkaError as e:
     print(f"Connection failed {e}")
"""

async def print_broadcast(payload):
    print(payload)



async def main():
    vehicle = Vehicle("vehicle-1")
    await vehicle.simulate_vehicle(print_broadcast)


if __name__ == "__main__":
    asyncio.run(main())