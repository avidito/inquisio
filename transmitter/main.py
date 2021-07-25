from sink import get_consumer
from utils import get_params, logging
from processor import process_data

if __name__ == "__main__":
    params = get_params()
    topic = params["TOPIC"]
    bootstrap_server = params["BOOTSTRAP_SERVER"]


    logging(f"Start sink with: {params}")
    consumer = get_consumer(bootstrap_server)
    # producer = get_producer()
    while(1):
        try:
            consumer.subscribe([topic])
            if (consumer):
                for result in consumer:
                    prc_data = process_data(result.value)
                    print(prc_data)
        except KeyboardInterrupt:
            logging("Receive termination signal")
            break

    logging("Closing consumer job")
