import json
import logging
import time


def run(training_data: dict) -> dict:
    training_id = training_data['trainingId']
    dataset_uri = training_data['datasetUri']
    logging.info(
        "Training started - trainingId: %s, datasetUri: %s", training_id, dataset_uri)
    time.sleep(30)
    metrics = {'metric-a': 1, 'metric-b': 2}
    logging.info(
        "Training finished - trainingId: %s, datasetUri: %s, metrics: %s", training_id, dataset_uri, json.dumps(metrics))
    return metrics
