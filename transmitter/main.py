from sink import get_consumer
from utils import get_params, logging

if __name__ == "__main__":
    params = get_params()
    topic = params["TOPIC"]
    bootstrap_server = params["BOOTSTRAP_SERVER"]
    path = params["TMP_PATH"]

    logging(f"Start sink with: {params}")
    consumer = get_consumer(bootstrap_server)
    while(1):
        try:
            consumer.subscribe([topic])
            if (consumer):
                for result in consumer:
                    print(result.value)
        except KeyboardInterrupt:
            logging("Receive termination signal")
            break

    logging("Closing consumer job")
