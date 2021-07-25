from sink import get_consumer
from producer import get_producer
from utils import get_params, logging
from processor import process_data

if __name__ == "__main__":
    logging(f"Start sink job")
    sink_params, transmitter_params = get_params()
    consumer, topic = get_consumer(sink_params)
    producer = get_producer(transmitter_params)

    while(1):
        try:
            consumer.subscribe([topic])
            if (consumer):
                for result in consumer:
                    prc_data = process_data(result.value)
                    print(prc_data)
                    producer.publish_data(prc_data)
        except KeyboardInterrupt:
            logging("Receive termination signal")
            break

    logging("Closing consumer job")
