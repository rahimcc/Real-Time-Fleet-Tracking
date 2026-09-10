
import json
import redis

from kafka import KafkaConsumer
from threading import Thread




r = redis.Redis(host="localhost", port = 6379, decode_responses = True )


def consume_driver_locations():

    consumer = KafkaConsumer( 
                "driver-locations",
                bootstrap_servers = "localhost:9092",
                value_deserializer = lambda v: json.loads(v.decode("utf-8")),
                key_deserializer = lambda k: k.decode("utf-8")
    )

    for msg in consumer:
        event = msg.value

        r.hset("drivers:live", event["driver_id"], json.dumps(event))
        r.publish("drivers:update", json.dumps(event))


def consume_order_events():

    consumer = KafkaConsumer( 
                "order-events",
                bootstrap_servers="localhost:9092",
                value_deserializer= lambda v: json.loads(v.decode("utf-8")),
                group_id = "redis-write"
        )

    for msg in consumer:
        event = msg.value

        r.hset("orders:live", event["order_id"], json.dumps(event))
        r.publish("orders:update", json.dumps(event))




if __name__ == "__main__":

    Thread(target=consume_driver_locations, daemon= True).start()
    Thread(target=consume_order_events, daemon=True).start()

    print("Consuming into Redis... Cntrl + C to stop ")

    while True:
        pass









