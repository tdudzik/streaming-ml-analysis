import api
import json
import time
from config import BaseDb
from datetime import datetime
from sqlalchemy import BigInteger, Column, String
from sqlalchemy.sql import text


class Training(BaseDb):
    __tablename__ = "trainings"

    training_id = Column(String, primary_key=True)
    dataset_id = Column(String)
    dataset_name = Column(String)
    status = Column(String)
    metrics = Column(String)
    created_at = Column(BigInteger, server_default=text(
        f"(CAST(strftime('%s', 'now') AS INT))"))
    completed_at = Column(BigInteger)

    STATUS_QUEUED = 'QUEUED'
    STATUS_IN_PROGRESS = 'IN_PROGRESS'
    STATUS_COMPLETED = 'COMPLETED'
    STATUS_FAILED = 'FAILED'

    def to_json(self) -> dict:
        return {
            'trainingId': self.training_id,
            'datasetId': self.dataset_id,
            'datasetName': self.dataset_name,
            'status': self.status,
            'createdAt': self.created_at,
            'completedAt': self.completed_at,
            'metrics': {} if self.metrics is None else self.metrics
        }

    def to_api_response(self) -> api.TrainingResponse:
        return api.TrainingResponse(
            training_id=self.training_id,
            dataset_id=self.dataset_id,
            dataset_name=self.dataset_name,
            status=self.status,
            created_at=datetime.fromtimestamp(
                self.created_at).strftime("%Y-%m-%d %H:%M:%S"),
            completed_at=None if self.completed_at is None else datetime.fromtimestamp(
                self.completed_at).strftime("%Y-%m-%d %H:%M:%S"),
            metrics=None if self.metrics is None else json.loads(self.metrics)
        )

    def in_progress(self) -> None:
        self.status = Training.STATUS_IN_PROGRESS

    def complete(self, metrics: dict) -> None:
        self.status = Training.STATUS_COMPLETED
        self.metrics = json.dumps(metrics)
        self.completed_at = int(time.time())

    def fail(self) -> None:
        self.status = Training.STATUS_FAILED
