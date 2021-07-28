from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
import time
import json

def get_producer(params):
    """Get producer instance"""

    topic = params.get("TRANSMITTER_TOPIC")
    bootstrap_server = params.get("TRANSMITTER_BOOTSTRAP_SERVER")

    _producer = KafkaProducer(
        bootstrap_servers = [bootstrap_server],
        value_serializer = lambda x : bytes(json.dumps(x), encoding="utf-8", errors="ignore")
    )
    return Producer(_producer, topic)

class Producer:
    """KafkaProducer object wrapper for scraper result"""

    def __init__(self, producer, topic):
        self.producer = producer
        self.topic = topic

    def publish_data(self, data):
        """Publishing JSON data to topic"""

        tries = 1
        while(tries <= 5):
            try:
                self.producer.send(self.topic, value=data)
                self.producer.flush()
                break

            except NoBrokersAvailable as e:
                print(f"Error while publishing data to {self.topic} topic. Retry in 5 seconds. Attempt : {tries}")
                time.sleep(5)
                tries += 1
