import api
from config import BaseDb
from sqlalchemy import Column, String


class Training(BaseDb):
    __tablename__ = "trainings"

    training_id = Column(String, primary_key=True)
    dataset_id = Column(String)
    status = Column(String)

    STATUS_QUEUED = 'QUEUED'
    STATUS_IN_PROGRESS = 'IN_PROGRESS'
    STATUS_COMPLETED = 'COMPLETED'
    STATUS_FAILED = 'FAILED'

    def to_json(self) -> dict:
        return {'trainingId': self.training_id, 'datasetId': self.dataset_id, 'status': self.status}

    def to_api_response(self) -> api.TrainingResponse:
        return api.TrainingResponse(training_id=self.training_id, dataset_id=self.dataset_id, status=self.status)

    def complete(self) -> None:
        self.status = Training.STATUS_COMPLETED

    def fail(self) -> None:
        self.status = Training.STATUS_FAILED
