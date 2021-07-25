from kafka import KafkaConsumer

def get_consumer(bootstrap_server):
    """Get consumer result from subscription"""

    consumer = KafkaConsumer(
        bootstrap_servers = bootstrap_server,
        value_deserializer = lambda x: x.decode("utf-8")
    )
    return consumer
