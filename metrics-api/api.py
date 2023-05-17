from config import BaseApi


class MetricsRequest(BaseApi):
    training_id: str
    metrics: dict


class MetricsResponse(BaseApi):
    metrics_id: str
    training_id: str
    metrics: dict
