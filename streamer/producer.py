from kafka import KafkaProducer

def get_producer(params):

    topic = params.get("TOPIC")
    bootstrap_server = params.get("BOOTSTRAP_SERVER")
    _producer = KafkaProducer(bootstrap_server=bootstrap_server)

    return Producer(_producer, topic)

class Producer:
    def __init__(self, producer, topic):
        self.producer = producer
        self.topic = topic

    def publish_data(self, data):
        tries = 0
        while(tries < 5):
            try:
                data_byte = bytes(str(data), encoding="utf-8")
                self.producer.send(data_byte)
                self.producer.flush()

                break
            except:
                tries += 1
