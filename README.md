# Real-Time-Fleet-Tracking


> 🚧 **Work in progress** — this is an evolving portfolio project. Currently
> implements a single simulated vehicle tracked live on a map; the full
> multi-vehicle, Kafka-based pipeline is under active development. See
> [Roadmap](#roadmap) below for what's done vs. planned.

A real-time vehicle-tracking dashboard: a simulated vehicle emits GPS
updates, which stream to a live map over WebSocket. Eventually this will
grow into a full event-driven pipeline (Kafka → Redis → dashboard) tracking
a whole fleet of drivers and order deliveries.

## Demo

https://livefleet.site

## Architecture (planned)

```
producers (drivers, orders) ──▶ Kafka ──▶ consumer ──▶ Redis ──▶ FastAPI/WebSocket ──▶ browser
```

## Tech stack

- **Backend:** Python, FastAPI, WebSockets
- **Frontend:** MapLibre GL JS (vector map rendering)
- **Planned:** Apache Kafka, Redis, Docker Compose

## Running locally

```bash
git clone <your-repo-url>
cd fleet-tracking
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn server:app --host 0.0.0.0 --port 8000
```

Then open `http://localhost:8000` in your browser.

## Project structure

```
fleet-tracking/
├── server.py           # FastAPI app: serves the page + WebSocket endpoint
├── requirements.txt
└── static/
    └── index.html       # MapLibre map + WebSocket client
```

## Roadmap

1. Reintroduce Kafka for event streaming (single broker, KRaft mode)
2. Add Redis as the live-state store between Kafka and the dashboard
3. Scale from one simulated vehicle to a full fleet of drivers
4. Add order lifecycle events alongside driver tracking
5. Stretch goals: windowed aggregation, idle-driver detection, schema
   registry, dead-letter topics, Postgres historical sink

## License

*MIT*
