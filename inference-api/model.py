import api
import json
from config import BaseDb
from datetime import datetime
from sqlalchemy import BigInteger, Boolean, Column, Integer, String
from sqlalchemy.sql import text


class Inference(BaseDb):
    __tablename__ = "inferences"

    inference_id = Column(String, primary_key=True)
    name = Column(String)
    data = Column(String)
    result = Column(Boolean)
    created_at = Column(BigInteger, server_default=text(
        f"(CAST(strftime('%s', 'now') AS INT))"))

    def to_api_response(self) -> api.InferenceResponse:
        return api.InferenceResponse(
            inference_id=self.inference_id,
            name=self.name,
            data=json.loads(self.data),
            result=self.result,
            created_at=datetime.utcfromtimestamp(
                self.created_at).isoformat() + 'Z'
        )
