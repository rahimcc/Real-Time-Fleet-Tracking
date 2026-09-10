import asyncio
import json
import redis.asyncio as aredis
import random
import time

from fastapi import FastAPI , WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles 



app = FastAPI()

connected_clients: set[WebSocket] = set()


vehicle = { 
    "lat": 40.4093,
    "lon": 49.8671,
    "speed_km": 0,
    "heading": random.uniform(0,360)
}

@app.get("/", response_class=HTMLResponse)
async def index():
    with open("static/index-3.html") as f:
        return f.read()


@app.websocket("/ws")
async def web_socketendpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)

    try:
        while True: 
            await websocket.receive_text()

    except WebSocketDisconnect:
        connected_clients.discard(websocket)


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
 
@app.on_event("startup")
async def startup():
    print("STARTUP: creating simulate_vehicle task")
    asyncio.create_task(simulate_vehicle())
    print("STARTUP: task created")
 