import json
import uuid
from api import TrainingRequest, TrainingResponse
from config import app, get_db, init_db, redis
from model import Training
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from typing import Callable


init_db()


TRAINING_STATE_KEY = 'training_state'


@app.get('/trainings', response_model=list[TrainingResponse])
def get_all_trainings(db: Session = Depends(get_db)):
    return [training.to_api_response() for training in db.query(Training).all()]


@app.post('/trainings', response_model=TrainingResponse)
def create_training(training_request: TrainingRequest, db: Session = Depends(get_db)):
    # Check if any training is already in progress, if so, then return an error
    training_state = redis.get(TRAINING_STATE_KEY)
    if training_state == Training.STATUS_IN_PROGRESS:
        raise HTTPException(
            status_code=400, detail="A training is currently in progress")

    # Change training state to 'in progress'
    redis.set(TRAINING_STATE_KEY, Training.STATUS_IN_PROGRESS)

    # Create a new training
    training = Training(
        training_id=str(uuid.uuid4()), dataset_id=training_request.dataset_id, status=Training.STATUS_QUEUED)

    # Save training to a db and publish it
    db.add(training)
    db.commit()
    db.refresh(training)
    redis.publish('trainings', json.dumps(training.to_json()))

    return training.to_api_response()


@app.get('/trainings/{training_id}', response_model=TrainingResponse)
def get_training(training_id: str, db: Session = Depends(get_db)):
    return __get_training(db, training_id).to_api_response()


@app.post('/trainings/{training_id}/complete', response_model=TrainingResponse)
def complete_training(training_id: str, db: Session = Depends(get_db)):
    return __update_training(db, training_id, lambda training: training.complete())


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