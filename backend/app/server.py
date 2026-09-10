import asyncio
import json
import random
import time

from fastapi import FastAPI , WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from backend.producers.vehicle_simulator import simulate_vehicle




connected_clients: set[WebSocket] = set()

app = FastAPI()

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


async def broadcast(payload): 
    dead = set()

    for client in connected_clients:

        try:
            await client.send_text(payload)
            print(f"broadcasting to {len(connected_clients)} client(s): {payload}")
        except Exception:
            dead.add(client)
            connected_clients.difference_update(dead)


@app.on_event("startup")
async def startup():
    print("STARTUP: creating simulate_vehicle task")
    asyncio.create_task(simulate_vehicle(broadcast))
    print("STARTUP: task created")
 