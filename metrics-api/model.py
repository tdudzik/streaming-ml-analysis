import api
import json
from config import BaseDb
from sqlalchemy import Column, String


class Metrics(BaseDb):
    __tablename__ = "metrics"

    metrics_id = Column(String, primary_key=True)
    training_id = Column(String)
    metrics = Column(String)

    def to_api_response(self) -> api.MetricsResponse:
        return api.MetricsResponse(metrics_id=self.metrics_id, training_id=self.training_id, metrics=json.loads(self.metrics))
