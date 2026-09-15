import asyncio
from backend.producers.producer_drivers import Vehicle, print_broadcast



async def run_fleet(vehicle_ids):
    vehicles = [Vehicle(vid) for vid in vehicle_ids]
    tasks = [v.simulate_vehicle(print_broadcast) for v in vehicles]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    vehicle_ids = [f"vehicle-{i}" for i in range(5)]
    print("Running 5 vehicles")
    asyncio.run(run_fleet(vehicle_ids))