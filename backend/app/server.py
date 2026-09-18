import asyncio
import json
import random
import time
import os

from fastapi import FastAPI , WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from backend.producers.vehicle_simulator import simulate_vehicle
from backend.producers.producer_drivers import Vehicle
from fastapi.staticfiles import StaticFiles
import redis.asyncio as aredis

connected_clients: set[WebSocket] = set()
app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

r = aredis.Redis(host='redis', port = 6379, decode_responses=True)


@app.get("/", response_class=HTMLResponse)
async def index():
    with open("frontend/static/index-3.html") as f:
        return f.read()


@app.get("/api/vehicle/state")
async def state():
    vehicles = await r.hgetall("vehicle:live")
    return {"vehicles": {k: json.loads(v) for k, v in vehicles.items()}}

@app.get("/api/train/state")
async def state():
    vehicles = await r.hgetall("vehicle:live")
    return {"vehicles": {k: json.loads(v) for k, v in vehicles.items()}}




@app.websocket("/ws")
async def web_socketendpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    print("Client connected")
    print( connected_clients)

    try:
        while True: 
            await websocket.receive_text()

    except WebSocketDisconnect:
        connected_clients.discard(websocket)

async def redis_listener():
    pubsub = r.pubsub()
    await pubsub.subscribe("vehicle:update","train:update")

    async for message in pubsub.listen():

        if message["type"] != "message":
            print(f"Dropped: {message}")
            continue

        dead = set()
        print(message)
        for client in connected_clients:
            try:
                await client.send_text(json.dumps(message))
            except Exception:
                dead.add(client)

        connected_clients.difference_update(dead)


@app.on_event("startup")
async def startup():
    print("STARTUP: creating simulate_vehicle task")
    asyncio.create_task(redis_listener())
    print("STARTUP: task created")
 