import logging
import os


TRAINING_API_URL = os.environ['TRAINING_API_URL'] if 'TRAINING_API_URL' in os.environ else ''

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)
