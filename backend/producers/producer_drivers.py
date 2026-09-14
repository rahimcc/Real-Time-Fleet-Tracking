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
from backend.app.server import broadcast
import asyncio



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

    
    








ECONDS_PER_HOUR = 3600
KM_PER_DEGREE_LATITUDE = 111 


vehicle = { 
    "lat": 40.4093,
    "lon": 49.8671,
    "heading": random.uniform(0,360)
}



#logging.basicConfig(level=logging.DEBUG)

host = "localhost"
port = 9092

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

try:
    producer = KafkaProducer( 
          bootstrap_servers=BOOTSTRAP ,
          value_serializer=lambda v: json.dumps(v).encode('utf-8'),
          key_serializer=lambda k: k.encode('utf-8')
    )
    print("Bootstrap connected: ", producer.bootstrap_connected())

except KafkaError as e:
     print(f"Connection failed {e}")

def start_new_trip(): 
    """
    Randomly pick two metro stations and calculate route

    Args: 


    Returns: 

        dict: 
    """

    global route, route_index , vehicle , start_name, end_name, start_coord, end_coord

    start_name , end_name = pick_random_trip() 

    start_coord = BAKU_METRO_STATIONS[start_name]
    end_coord = BAKU_METRO_STATIONS[end_name]

    vehicle['lat'] , vehicle['lon'] = start_coord


    new_route = fetch_route(start_coord[0],start_coord[1],end_coord[0], end_coord[1])
    if new_route: 
        route = new_route 
        route_index = 0
        print(f'new trip: {start_name} -> {end_name} ({len(route)} points)')
        print(route)

    else: 
        print(f'Failed to fetch route from {start_name} to {end_name}, retrying next tick')





async def simulate_vehicle(broadcast) -> None:
    """Moves the vehicle a small random step every second"""

    global route_index , route

    start_new_trip()
    print("New trip was created")


    while True:
        try:
            if not route:
                print(f'Not route: {route}')
                start_new_trip()
                await asyncio.sleep(1)


            if route_index >= len(route):
                print(f'Route index bigger.')

                print(f'Route len= {len(route)}')
                print(f'Route index = {route_index}')
                start_new_trip()
                await asyncio.sleep(1)
                continue


            lon, lat = route[route_index]
            vehicle['lat'] = lat
            vehicle['lon'] = lon
            route_index += 1
            print('Route index icremented')
            payload = json.dumps({
                "lat": round(vehicle['lat'],6),
                "lon": round(vehicle['lon'],6),
                "heading": vehicle["heading"],
                "trip":  f'{start_name} -> {end_name}',
                "start_lat": start_coord[0], "start_lon": start_coord[1],
                "end_lat": end_coord[0], "end_lon": end_coord[1],
                "timestamp": time.time() 
            })

            print(payload)

            # await broadcast(payload)
            await asyncio.sleep(1)

        except Exception as e:
            print(f'simulate_vehicle loop error: {e}')
            break
            
    await asyncio.sleep(1)


test_kafka(host=host,port=port)

simulate_vehicle(broadcast)
