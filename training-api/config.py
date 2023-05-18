import logging
import os
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from humps import camelize
from pydantic import BaseModel
from redis import Redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Constants
DATABASE_URL = "sqlite:///./trainings.db"
REDIS_URL = os.environ['REDIS_URL']
DATASET_API_URL = os.environ['DATASET_API_URL']
TRAINING_API_URL = os.environ['TRAINING_API_URL']


# Logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)


# Database
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
BaseDb = declarative_base()


def init_db() -> None:
    BaseDb.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# API
def to_camel(string):
    return camelize(string)


class BaseApi(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


# App
app = FastAPI()
origins = [
    "http://localhost:8081"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Redis
redis = Redis.from_url(REDIS_URL, decode_responses=True)


# Scheduler
scheduler = BackgroundScheduler()
scheduler.start()
