
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




