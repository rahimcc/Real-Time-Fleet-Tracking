import asyncio
from backend.producers.producer_drivers import Vehicle


async def print_broadcast(payload):
    print(payload)


async def main():
    vehicle = Vehicle("vehicle-1")
    await vehicle.simulate_vehicle(print_broadcast)


if __name__ == "__main__":
    asyncio.run(main())