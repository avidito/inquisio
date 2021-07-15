from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
import time

def get_producer(params):
    """Get producer instance"""
    topic = params.get("TOPIC")
    bootstrap_server = params.get("BOOTSTRAP_SERVER")
    _producer = KafkaProducer(bootstrap_servers=[bootstrap_server])

    return Producer(_producer, topic)

class Producer:
    """KafkaProducer object wrapper for scraper result"""
    def __init__(self, producer, topic):
        self.producer = producer
        self.topic = topic

    def publish_data(self, data):
        tries = 1
        data_byte = bytes(json.dumps(data), encoding="utf-8")
        while(tries <= 5):
            try:
                self.producer.send(self.topic, value=data_byte)
                self.producer.flush()
                break

            except NoBrokersAvailable as e:
                print(f"Error while publishing data to {self.topic} topic. Retry in 5 seconds. Attempt : {tries}")
                time.sleep(5)
                tries += 1
