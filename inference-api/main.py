import json
import uuid
from api import InferenceRequest, InferenceResponse
from config import app, get_db, init_db
from dateutil import parser
from model import Inference
from fastapi import Depends, Query
from logger import logger
from sqlalchemy import asc
from sqlalchemy.orm import Session


init_db()


@app.get('/inferences', response_model=list[InferenceResponse])
def get_all_trainings(
    db: Session = Depends(get_db),
    from_time: str = Query(None),
    to_time: str = Query(None)
):
    query = db.query(Inference)

    if from_time:
        from_created_at = int(parser.parse(from_time).timestamp())
        query = query.filter(Inference.created_at >= from_created_at)
    if to_time:
        to_created_at = int(parser.parse(to_time).timestamp())
        query = query.filter(Inference.created_at <= to_created_at)

    query = query.order_by(asc(Inference.created_at))

    return [inference.to_api_response() for inference in query.all()]


@app.post('/inferences', response_model=InferenceResponse)
def create_training(inference_request: InferenceRequest, db: Session = Depends(get_db)):
    # Create a new inference
    inference = Inference(
        inference_id=str(uuid.uuid4()),
        name=inference_request.name,
        data=json.dumps(inference_request.data),
        result=inference_request.result
    )

    # Save training to a db and publish it
    db.add(inference)
    db.commit()
    db.refresh(inference)

    return inference.to_api_response()
