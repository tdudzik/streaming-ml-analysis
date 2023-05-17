import json
import uuid
from api import MetricsRequest, MetricsResponse
from config import app, get_db, init_db
from model import Metrics
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound


init_db()


@app.get('/metrics', response_model=list[MetricsResponse])
def get_all_metrics(db: Session = Depends(get_db)):
    return [metrics.to_api_response() for metrics in db.query(Metrics).all()]


@app.post('/metrics', response_model=MetricsResponse)
def create_metrics(metrics_request: MetricsRequest, db: Session = Depends(get_db)):
    # Create new metrics
    metrics = Metrics(
        metrics_id=str(uuid.uuid4()), training_id=metrics_request.training_id, metrics=json.dumps(metrics_request.metrics))

    # Save metrics to a db
    db.add(metrics)
    db.commit()
    db.refresh(metrics)

    return metrics.to_api_response()


@app.get('/metrics/{metrics_id}', response_model=MetricsResponse)
def get_metrics(metrics_id: str, db: Session = Depends(get_db)):
    return __get_metrics(db, metrics_id).to_api_response()


def __get_metrics(db: Session, metrics_id: str) -> Metrics:
    try:
        return db.query(Metrics).filter(
            Metrics.metrics_id == metrics_id).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Training not found")
