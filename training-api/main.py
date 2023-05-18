import json
import requests
import time
import uuid
from api import ScheduleTrainingRequest, TrainingCompleteRequest, TrainingIntervalUnit, TrainingRequest, TrainingResponse, TrainingScheduleResponse
from config import app, get_db, init_db, redis, scheduler, DATASET_API_URL, TRAINING_API_URL
from datetime import datetime
from model import Training
from fastapi import Depends, HTTPException
from sqlalchemy import asc
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from typing import Callable


init_db()


TRAINING_STATE_KEY = 'training_state'
TRAINING_SCHEDULE_KEY = 'training_schedule'


@app.get('/trainings', response_model=list[TrainingResponse])
def get_all_trainings(db: Session = Depends(get_db)):
    return [training.to_api_response() for training in db.query(Training).order_by(asc(Training.created_at)).all()]


@app.post('/trainings', response_model=TrainingResponse)
def create_training(training_request: TrainingRequest, db: Session = Depends(get_db)):
    # Check if any training is already in progress, if so, then return an error
    training_state = redis.get(TRAINING_STATE_KEY)
    if training_state == Training.STATUS_IN_PROGRESS:
        raise HTTPException(
            status_code=400, detail="A training is currently in progress")

    # Get dataset
    dataset_response = requests.get(__dataset_api_url(
        f'/datasets/{training_request.dataset_id}'))
    if dataset_response.status_code != 200:
        raise HTTPException(status_code=400, detail="Dataset not found")
    dataset = dataset_response.json()

    # Change training state to 'in progress'
    redis.set(TRAINING_STATE_KEY, Training.STATUS_IN_PROGRESS)

    # Create a new training
    training = Training(
        training_id=str(uuid.uuid4()), dataset_id=dataset['datasetId'], dataset_name=dataset['name'], status=Training.STATUS_QUEUED, metrics=None)

    # Save training to a db and publish it
    db.add(training)
    db.commit()
    db.refresh(training)
    redis.publish('trainings', json.dumps(
        {'trainingId': training.training_id, 'datasetUri': dataset['uri']}))

    return training.to_api_response()


@app.post('/trainings/schedule', response_model=TrainingScheduleResponse)
def schedule_training(schedule_training_request: ScheduleTrainingRequest):
    scheduler.remove_all_jobs()
    redis.delete(TRAINING_SCHEDULE_KEY)
    if schedule_training_request.interval_unit == TrainingIntervalUnit.MINUTES:
        scheduler.add_job(__create_training, 'interval',
                          minutes=schedule_training_request.interval)
    elif schedule_training_request.interval_unit == TrainingIntervalUnit.HOURS:
        scheduler.add_job(__create_training, 'interval',
                          hours=schedule_training_request.interval)
    elif schedule_training_request.interval_unit == TrainingIntervalUnit.DAYS:
        scheduler.add_job(__create_training, 'interval',
                          days=schedule_training_request.interval)
    else:
        raise HTTPException(status_code=422, detail="Invalid interval unit")
    created_at = int(time.time())
    training_schedule_response = TrainingScheduleResponse(
        interval=schedule_training_request.interval,
        interval_unit=schedule_training_request.interval_unit.value,
        created_at=datetime.fromtimestamp(
            created_at).strftime("%Y-%m-%d %H:%M:%S")
    )
    redis.set(TRAINING_SCHEDULE_KEY, training_schedule_response.json())

    return training_schedule_response


@app.delete('/trainings/schedule')
def cancel_training_schedule():
    scheduler.remove_all_jobs()
    redis.delete(TRAINING_SCHEDULE_KEY)


@app.get('/trainings/schedule', response_model=TrainingScheduleResponse)
def get_training_schedule():
    training_schedule_json = redis.get(TRAINING_SCHEDULE_KEY)
    if training_schedule_json is None:
        raise HTTPException(
            status_code=404, detail="Training schedule not found")
    training_schedule = json.loads(training_schedule_json)
    training_schedule_response = TrainingScheduleResponse(
        interval=training_schedule['interval'],
        interval_unit=training_schedule['interval_unit'],
        created_at=training_schedule['created_at']
    )
    return training_schedule_response


@app.get('/trainings/{training_id}', response_model=TrainingResponse)
def get_training(training_id: str, db: Session = Depends(get_db)):
    return __get_training(db, training_id).to_api_response()


@app.post('/trainings/{training_id}/in-progress', response_model=TrainingResponse)
def training_in_progress(training_id: str, db: Session = Depends(get_db)):
    return __update_training(db, training_id, lambda training: training.in_progress())


@app.post('/trainings/{training_id}/complete', response_model=TrainingResponse)
def complete_training(training_id: str, complete_request: TrainingCompleteRequest, db: Session = Depends(get_db)):
    return __update_training(db, training_id, lambda training: training.complete(complete_request.metrics))


@app.post('/trainings/{training_id}/fail', response_model=TrainingResponse)
def fail_training(training_id: str, db: Session = Depends(get_db)):
    return __update_training(db, training_id, lambda training: training.fail())


def __get_training(db: Session, training_id: str) -> Training:
    try:
        return db.query(Training).filter(
            Training.training_id == training_id).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Training not found")


def __update_training(db: Session, training_id: str, update: Callable[[Training], None]) -> TrainingResponse:
    training = __get_training(db, training_id)
    update(training)
    db.commit()
    db.refresh(training)
    return training.to_api_response()


def __create_training():
    dataset_response = requests.get(
        __dataset_api_url(f'/datasets/latest')).json()
    dataset_id = dataset_response['datasetId']
    requests.post(__training_api_url('/trainings'),
                  json={'datasetId': dataset_id})


def __dataset_api_url(path) -> str:
    return DATASET_API_URL + path


def __training_api_url(path) -> str:
    return TRAINING_API_URL + path
