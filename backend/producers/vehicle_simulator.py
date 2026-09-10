import json
import time


vehicle = { 
    "lat": 40.4093,
    "lon": 49.8671,
    "speed_km": 0,
    "heading": random.uniform(0,360)
}


async def simulate_vehicle():
    """Moves the vehicle a small random step every second"""

    while True: 

       # print(" STEP 1: entering loop iteration")
        if random.random() < 0.1:
            vehicle['heading'] += random.uniform(-45,45)

        vehicle['speed_km'] = round(random.uniform(120,160),1)

        step = vehicle['speed_km'] / 3600 / 111 * 200


        vehicle["lat"] += step * random.uniform(10, 12) * _cos(vehicle["heading"])
        vehicle["lon"] += step * random.uniform(10, 12) * _sin(vehicle["heading"])
 
        payload = json.dumps({
            "lat": round(vehicle["lat"], 6),
            "lon": round(vehicle["lon"], 6),
            "speed_kmh": vehicle["speed_km"],
            "timestamp": time.time(),
        })


        # print(payload)

        dead = set()
        for client in connected_clients:
            try:
                await client.send_text(payload)
            except Exception:
                dead.add(client)
        connected_clients.difference_update(dead)
 
        await asyncio.sleep(1)
 
def _cos(deg):
    import math
    return math.cos(math.radians(deg))
 
def _sin(deg):
    import math
    return math.sin(math.radians(deg))