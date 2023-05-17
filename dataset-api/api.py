from config import BaseApi


class DatasetResponse(BaseApi):
    dataset_id: str
    uri: str
