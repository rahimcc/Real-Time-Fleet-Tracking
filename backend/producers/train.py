import json
from kafka import KafkaProducer
from backend.services.logger import setup_logger
import asyncio
import time
from pathlib import Path



class Train:

    def __init__(self, train_id):
        self.train_id = train_id
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


    def load_train_route(self):

        GEOJSON_PATH = Path(__file__).parent.parent / "static/Baku_Bilajari.geojson"


        with open(GEOJSON_PATH,"r") as f:
            geojson_data = json.load(f)


        #print(geojson_data)
        coordinates = geojson_data["features"][0]["geometry"]["coordinates"]
        route = [{"lat": lat, "lon": lon} for lon,lat in coordinates]

        return route


    def start_new_trip(self) -> None:

        self.start_name, self.end_name = "Bakı Vağzalı", "Biləcəri"


        # Fetch route between these two coordinates
        new_route = self.load_train_route() 


        if new_route: 
           self.route = new_route 
           self.route_index = 0
           print(f'New trip: {self.start_name} -> {self.end_name} ({len(self.route)} points)')
           #print(route)
        else: 
            print(f'Failed to fetch route from {self.start_name} to {self.end_name}, retrying next tick')



    async def simulate_vehicle(self) -> None:
            """Moves the vehicle a small random step every second"""


            self.start_new_trip()
            producer = KafkaProducer( 
                                    bootstrap_servers="kafka:9092",
                                    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                                    key_serializer=lambda k: k.encode("utf-8")
                                )

            print(self.route)
            logger = setup_logger('producer')
    
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
    
    
                    self.lat, self.lon = self.route[self.route_index].values()

                    print(self.lon, self.lon)
    
                    self.route_index += 1
                    print('Route index icremented')
    
                    payload = {
                        "train-id": self.train_id,
                        "lat": round(self.lat,6),
                        "lon": round(self.lon,6),
                        "heading": self.heading,
                        "trip":  f'{self.start_name} -> {self.end_name}',
                        "start_lat": 0, "start_lon": 0,
                        "end_lat": 0, "end_lon": 0,
                        "timestamp": time.time(),
                        "test": "test"
                    }
    
                   # print(payload)
                  
                    
                    
                    producer.send("train-locations", key=self.train_id, value=payload)
                    producer.flush()
                    print("Event sent to Kafka")
    
                    logger.info(payload)
                    
                    await asyncio.sleep(1)
    
                except Exception as e:
                    print(f'simulate_vehicle loop error: {e}')
                    break
                    
            await asyncio.sleep(1)