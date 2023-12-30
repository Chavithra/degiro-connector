from datetime import datetime, timedelta
from typing import Literal

from pydantic import BaseModel, Field

from degiro_connector.quotecast.models.metric import MetricType


class Ticker(BaseModel):
    """Text JSON message received from Degiro's Quotecast API."""

    json_text: str
    response_datetime: datetime = Field(default_factory=datetime.now)
    request_duration: timedelta


class TickerRequest(BaseModel):
    request_type: Literal["subscription", "unsubscription"]
    request_map: dict[str, list[MetricType]] | dict[str, list[str]]
