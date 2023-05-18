from config import BaseApi
from enum import Enum


class TrainingRequest(BaseApi):
    dataset_id: str


class TrainingResponse(BaseApi):
    training_id: str
    dataset_id: str
    dataset_name: str
    status: str
    created_at: str
    metrics: dict | None


class TrainingCompleteRequest(BaseApi):
    metrics: dict


class TrainingIntervalUnit(Enum):
    MINUTES = "minutes"
    HOURS = "hours"
    DAYS = "days"


class ScheduleTrainingRequest(BaseApi):
    interval: int
    interval_unit: TrainingIntervalUnit


class TrainingScheduleResponse(BaseApi):
    interval: int
    interval_unit: str
    created_at: str
