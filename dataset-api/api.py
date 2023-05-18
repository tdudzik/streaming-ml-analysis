from config import BaseApi


class DatasetResponse(BaseApi):
    dataset_id: str
    name: str
    uri: str
    created_at: str
