from dask_ml.linear_model import LogisticRegression
from dask_ml.preprocessing import StandardScaler
from joblib import load
from kafka import KafkaConsumer
from logger import logger
import config
import inference
import json
import sys
import threading
import numpy as np
import pandas as pd
import requests
import os


model: LogisticRegression | None = None
scaler: StandardScaler | None = None
model_categories: list[str] | None = None
model_lock = threading.Lock()


def inference_api_url(path) -> str:
    return config.INFERENCE_API_URL + path


def consume_kickstarter_data(bootstrap_servers):
    consumer = KafkaConsumer(
        'kickstarter-data',
        bootstrap_servers=bootstrap_servers,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='inference-consumer',
        consumer_timeout_ms=120000
    )

    for message in consumer:
        decoded_message = message.value.decode('utf-8')
        message_json = json.loads(decoded_message)
        with model_lock:
            logger.info("Received kickstarter message: %s",
                        decoded_message)
            if model is not None and scaler is not None and model_categories is not None:
                data = message_json['data']
                df = pd.DataFrame.from_dict(data, orient='index').T
                result = inference.run(
                    model, scaler, model_categories, df)
                inference_data = {
                    'name': data['Name'],
                    'data': data,
                    'result': result
                }
                requests.post(inference_api_url(
                    '/inferences'), json=inference_data)
                logger.info("Prediction result: %s", result)


def consume_model_selection(bootstrap_servers):
    consumer = KafkaConsumer(
        'model-selection',
        bootstrap_servers=bootstrap_servers,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='model-selection-consumer',
        consumer_timeout_ms=120000
    )

    for message in consumer:
        training_id = json.loads(message.value.decode('utf-8'))['trainingId']
        new_model_uri = f"./model/{training_id}.joblib"
        new_scaler_uri = f"./model/{training_id}.scaler.joblib"
        new_model_categories_uri = f"./model/{training_id}.categories.json"
        new_model = load_model(new_model_uri)
        new_scaler = load_scaler(new_scaler_uri)
        with open(new_model_categories_uri) as f:
            new_model_categories = json.load(f)
        logger.info("Received model selection message: %s",
                    message.value.decode('utf-8'))
        with model_lock:
            global model
            global scaler
            global model_categories
            model = new_model
            scaler = new_scaler
            model_categories = new_model_categories


def load_model(path: str):
    return load(path)


def load_scaler(path: str):
    return load(path)


if __name__ == '__main__':
    print("Consumers started")
    if len(sys.argv) < 2:
        print("Usage: python main.py <host> <port>")
        sys.exit(1)
    host = sys.argv[1]
    port = sys.argv[2]
    bootstrap_servers = host + ':' + port

    thread1 = threading.Thread(
        target=consume_kickstarter_data, args=(bootstrap_servers,))
    thread2 = threading.Thread(
        target=consume_model_selection, args=(bootstrap_servers,))
    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()
