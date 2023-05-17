import api
from config import BaseDb
from sqlalchemy import Column, String


class Dataset(BaseDb):
    __tablename__ = "datasets"

    dataset_id = Column(String, primary_key=True)
    uri = Column(String)

    def to_api_response(self) -> api.DatasetResponse:
        return api.DatasetResponse(dataset_id=self.dataset_id, uri=self.uri)
