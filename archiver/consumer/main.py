from kafka import KafkaConsumer

from utils import logging, get_params, export_data

def get_consumer(bootstrap_server):
    """Get consumer result from subscription"""

    consumer = KafkaConsumer(
        bootstrap_servers = bootstrap_server,
        value_deserializer = lambda x: x.decode("utf-8", "ignore")
    )
    return consumer

########## MAIN ##########
if __name__ == "__main__":
    params = get_params()
    topic = params["TOPIC"]
    bootstrap_server = params["BOOTSTRAP_SERVER"]
    path = params["DMP_PATH"]

    logging(f"Start consumer with topic `{topic}`")
    consumer = get_consumer(bootstrap_server)
    while(1):
        try:
            consumer.subscribe([topic])
            if (consumer):
                for result in consumer:
                    export_data(result, path)
        except KeyboardInterrupt:
            logging("Receive termination signal")
            break

    logging("Closing consumer job")
