import config
import logging
import json
import os
import requests
import training
from redis import Redis


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)


redis = Redis.from_url(os.environ['REDIS_URL'], decode_responses=True)
pubsub = redis.pubsub()
pubsub.subscribe('trainings')


TRAINING_STATE_KEY = 'training_state'


def training_api_url(path) -> str:
    return config.TRAINING_API_URL + path


def run_training(training_data):
    try:
        training_id = training_data['trainingId']
        metrics = training.run(training_data)
        requests.post(training_api_url(
            '/trainings/' + training_id + '/complete'), json={'metrics': metrics})
    except Exception as e:
        logger.error('An error occurred: %s', str(e))
        requests.post(training_api_url(
            '/trainings/' + training_data['trainingId'] + '/fail'))
    redis.set(TRAINING_STATE_KEY, 'IDLE')


if __name__ == '__main__':
    logging.info("Training worker started")
    for message in pubsub.listen():
        if message['type'] == 'message':
            training_data = json.loads(message['data'])
            run_training(training_data)
    logging.info("Training worker stopped")
