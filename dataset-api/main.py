import shutil
import uuid
from api import DatasetResponse
from config import app, get_db, init_db
from model import Dataset
from fastapi import Depends, File, Form, HTTPException, UploadFile
from pathlib import Path
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound


init_db()


@app.get('/datasets', response_model=list[DatasetResponse])
def get_all_datasets(db: Session = Depends(get_db)):
    return [dataset.to_api_response() for dataset in db.query(Dataset).order_by(asc(Dataset.created_at)).all()]


@app.post("/datasets", response_model=DatasetResponse)
def create_dataset(name: str = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    dataset_id = str(uuid.uuid4())
    extension = Path(file.filename).suffix
    path = f"./data/{dataset_id}{extension}"
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    uri = "file://" + str(Path(path).absolute())
    dataset = Dataset(dataset_id=dataset_id, name=name, uri=uri)
    db.add(dataset)
    db.commit()
    db.refresh(dataset)
    return dataset.to_api_response()


@app.get('/datasets/latest', response_model=DatasetResponse)
def get_latest_dataset(db: Session = Depends(get_db)):
    dataset = db.query(Dataset).order_by(desc(Dataset.created_at)).first()
    if dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return dataset.to_api_response()


@app.get('/datasets/{dataset_id}', response_model=DatasetResponse)
def get_dataset(dataset_id: str, db: Session = Depends(get_db)):
    return __get_datasets(db, dataset_id).to_api_response()


def __get_datasets(db: Session, dataset_id: str) -> Dataset:
    try:
        return db.query(Dataset).filter(
            Dataset.dataset_id == dataset_id).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Dataset not found")
