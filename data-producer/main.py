from kafka import KafkaProducer
from logger import logger
import json
import sys
import time
import pandas as pd
import random


if __name__ == '__main__':
    print("Producer started")
    if len(sys.argv) < 2:
        print("Usage: python main.py <host> <port>")
        sys.exit(1)
    host = sys.argv[1]
    port = sys.argv[2]
    bootstrap_servers = host + ':' + port
    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers, max_block_ms=120000)
    topic = 'kickstarter-data'

    df = pd.read_csv('./kickstarter_inference_10000.csv')
    kickstarter_data = json.loads(df.to_json(orient='records'))

    while True:
        timestamp = round(time.time() * 1000)
        single_data = random.choice(kickstarter_data)
        data = {'timestamp': timestamp,
                'data': single_data}
        message = json.dumps(data)
        producer.send(topic, message.encode('utf-8'))
        producer.flush()
        logger.info("message sent: %s", message)
        time.sleep(1)
    producer.close()
