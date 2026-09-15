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
import redis.asyncio as aredis

connected_clients: set[WebSocket] = set()
app = FastAPI()
r = aredis.Redis(host='redis', port = 6379, decode_responses=True)


@app.get("/", response_class=HTMLResponse)
async def index():
    with open("frontend/static/index-3.html") as f:
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

async def redis_listener():
    pubsub = r.pubsub()
    await pubsub.subscribe("vehicle:update")

    async for message in pubsub.listen():

        print(message)
        if message["type"] != "message":
            continue

        dead = set()

        for client in connected_clients:
            try:
                await client.send_text(message['data'])
            except Exception:
                dead.add(client)

        connected_clients.difference_update(dead)


@app.on_event("startup")
async def startup():
    print("STARTUP: creating simulate_vehicle task")
    asyncio.create_task(redis_listener())
    print("STARTUP: task created")
 