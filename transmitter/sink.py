from kafka import KafkaConsumer

def get_consumer(params):
    """Get consumer result from subscription"""

    topic = params.get("SINK_TOPIC")
    bootstrap_server = params.get("SINK_BOOTSTRAP_SERVER")

    consumer = KafkaConsumer(
        bootstrap_servers = bootstrap_server,
        value_deserializer = lambda x: x.decode("utf-8", "ignore")
    )
    return consumer, topic
