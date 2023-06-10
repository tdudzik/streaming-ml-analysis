from config import BaseApi


class InferenceRequest(BaseApi):
    name: str
    data: dict
    result: bool


class InferenceResponse(BaseApi):
    inference_id: str
    name: str
    data: dict
    result: bool
    created_at: str
