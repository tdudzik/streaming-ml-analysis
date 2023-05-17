import json
import logging
import time


def run(training_data: dict) -> dict:
    training_id = training_data['trainingId']
    dataset_id = training_data['datasetId']
    logging.info(
        "Training started - trainingId: %s, datasetId: %s", training_id, dataset_id)
    time.sleep(2)
    metrics = {'metric-a': 1, 'metric-b': 2}
    logging.info(
        "Training finished - trainingId: %s, datasetId: %s, metrics: %s", training_id, dataset_id, json.dumps(metrics))
    return metrics
