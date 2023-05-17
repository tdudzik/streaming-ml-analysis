from config import BaseApi


class TrainingRequest(BaseApi):
    dataset_id: str


class TrainingResponse(BaseApi):
    training_id: str
    dataset_id: str
    status: str
