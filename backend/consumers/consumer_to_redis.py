
import json
import redis
import os
import time


from kafka import KafkaConsumer
from threading import Thread

BOOTSRAP = os.environ.get("KAFKA_BOOTSTRAP", "kafka:9092")
REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
TOPIC = "vehicle-locations"



r = redis.Redis(host=REDIS_HOST, port = 6379, decode_responses = True)


def consume_driver_locations():

    print('Connecting to Kafka')
    consumer = KafkaConsumer( 
                "vehicle-locations",
                bootstrap_servers = "kafka:9092",
                value_deserializer = lambda v: json.loads(v.decode("utf-8")),
                key_deserializer = lambda k: k.decode("utf-8"),
                group_id="redis-write",
                request_timeout_ms=10000
    )

    for msg in consumer:
        event = msg.value
       # print(event)
        r.hset("vehicle:live", event["vehicle-id"], json.dumps(event))
        r.publish("vehicle:update", json.dumps(event))

def consume_train_locations():

    print('Connecting to Kafka')

    consumer = KafkaConsumer( 
                "train-locations",
                bootstrap_servers = "kafka:9092",
                value_deserializer = lambda v: json.loads(v.decode("utf-8")),
                key_deserializer = lambda k: k.decode("utf-8"),
                group_id="redis-write",
                request_timeout_ms=10000
    )

    for msg in consumer:
        event = msg.value
        print(event)
        r.hset("train:live", event["train_id"], json.dumps(event))
        r.publish("train:update", json.dumps(event))


def consume_order_events():

    consumer = KafkaConsumer( 
                "vehicle-locations",
                bootstrap_servers="kafka:9092",
                value_deserializer= lambda v: json.loads(v.decode("utf-8")),
                group_id = "redis-write",
                request_timeout_ms=10000,
                api_version_auto_timeout_ms=10000
        )

    print(f"KafkaConsumer created successfully: {consumer}")
    print(f"Subscribed topics: {consumer.subscription()}")
    print(f"Assigned partitions: {consumer.assignment()}")

    for msg in consumer:
        event = msg.value
        print(event)
        r.hset("orders:live", event["order_id"], json.dumps(event))
        r.publish("orders:update", json.dumps(event))




if __name__ == "__main__":

    #Thread(target=consume_driver_locations, daemon= True).start()
    print("Consumer started")
    Thread(target=consume_driver_locations, daemon=True).start()
    Thread(target=consume_train_locations, daemon=True).start()

    while True: 
        print("Consuming into Redis")
        print("Sleeping 10 seconds")
        time.sleep(10)    









