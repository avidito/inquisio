from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
import time
import json

def get_producer(params):
    """Get producer instance"""

    topic = params.get("TOPIC")
    bootstrap_server = params.get("BOOTSTRAP_SERVER")
    active = params.get("ACTIVE")

    if (active):
        _producer = KafkaProducer(
            bootstrap_servers = [bootstrap_server],
            value_serializer = lambda x: json.dumps(x).encode("utf-8", "ignore")
        )
    else:
        _producer = None
    return Producer(_producer, topic)

class Producer:
    """KafkaProducer object wrapper for scraper result"""

    def __init__(self, producer, topic):
        self.producer = producer
        self.topic = topic
        self.active = True if (producer) else False

    def publish_data(self, data):
        """Publishing JSON data to topic"""

        if (not self.active):
            return None

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
