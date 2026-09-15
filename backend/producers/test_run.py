import asyncio
from backend.producers.producer_drivers import Vehicle
from kafka import KafkaProducer
import json




async def print_broadcast(payload):
    print(payload)


async def main():
    vehicle = Vehicle("vehicle-1")
    await vehicle.simulate_vehicle(print_broadcast)


if __name__ == "__main__":

    print("Test run for Kafka")
    producer = KafkaProducer( 
        bootstrap_servers="kafka:9092",
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )


    producer.send("vehicle-locations", value={"test": "hello"})
    producer.flush()
    print("sent")