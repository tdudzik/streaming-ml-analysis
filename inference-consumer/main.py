from kafka import KafkaConsumer
from logger import logger
import sys


if __name__ == '__main__':
    print("Consumer started")
    if len(sys.argv) < 2:
        print("Usage: python main.py <host> <port>")
        sys.exit(1)
    host = sys.argv[1]
    port = sys.argv[2]
    bootstrap_servers = host + ':' + port
    consumer = KafkaConsumer(
        'kickstarter-data',
        bootstrap_servers=bootstrap_servers,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='inference-consumer',
        consumer_timeout_ms=120000
    )

    for message in consumer:
        # we're going to use our model here to infere the results
        # and save the result to database
        logger.info("Received message: %s", message.value.decode('utf-8'))
