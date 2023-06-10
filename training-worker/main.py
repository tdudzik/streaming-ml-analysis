import config
import json
import os
import requests
import training
from config import logger
from redis import Redis


redis = Redis.from_url(os.environ['REDIS_URL'], decode_responses=True)
pubsub = redis.pubsub()
pubsub.subscribe('trainings')


TRAINING_STATE_KEY = 'training_state'


def training_api_url(path) -> str:
    return config.TRAINING_API_URL + path


def run_training(training_data):
    try:
        training_id = training_data['trainingId']
        requests.post(training_api_url(
            '/trainings/' + training_id + '/in-progress'))
        training_id = training_data['trainingId']
        dataset_uri = training_data['datasetUri']
        logger.info(
            "Training started - trainingId: %s, datasetUri: %s", training_id, dataset_uri)
        metrics = training.run(training_id, dataset_uri)
        logger.info(
            "Training finished - trainingId: %s, datasetUri: %s, metrics: %s", training_id, dataset_uri, json.dumps(metrics))
        requests.post(training_api_url(
            '/trainings/' + training_id + '/complete'), json={'metrics': metrics})
    except Exception as e:
        logger.error('An error occurred: %s', str(e))
        requests.post(training_api_url(
            '/trainings/' + training_data['trainingId'] + '/fail'))
    redis.set(TRAINING_STATE_KEY, 'IDLE')


if __name__ == '__main__':
    logger.info("Training worker started")
    for message in pubsub.listen():
        if message['type'] == 'message':
            training_data = json.loads(message['data'])
            run_training(training_data)
    logger.info("Training worker stopped")
