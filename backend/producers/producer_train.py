import json
import time
import random
from kafka import KafkaProducer
from kafka.errors import KafkaError
import socket
import logging
from backend.producers.train import Train
import asyncio





if __name__ == "__main__":
    train = Train('train-1')
    
    asyncio.run(train.simulate_vehicle())