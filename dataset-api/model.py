import api
from config import BaseDb
from datetime import datetime
from sqlalchemy import BigInteger, Column, String
from sqlalchemy.sql import text


class Dataset(BaseDb):
    __tablename__ = "datasets"

    dataset_id = Column(String, primary_key=True)
    name = Column(String)
    uri = Column(String)
    created_at = Column(BigInteger, server_default=text(
        f"(CAST(strftime('%s', 'now') AS INT))"))

    def to_api_response(self) -> api.DatasetResponse:
        return api.DatasetResponse(
            dataset_id=self.dataset_id,
            name=self.name,
            uri=self.uri,
            created_at=datetime.fromtimestamp(
                self.created_at).strftime("%Y-%m-%d %H:%M:%S")
        )
