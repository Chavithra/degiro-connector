from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class Interval(str, Enum):
    PT15S = "PT15S"
    PT30S = "PT30S"
    PT1M = "PT1M"
    PT5M = "PT5M"
    PT15M = "PT15M"
    PT30M = "PT30M"
    PT60M = "PT60M"
    PT1H = "PT1H"
    P1D = "P1D"
    P1W = "P1W"
    P1M = "P1M"
    P3M = "P3M"
    P6M = "P6M"
    P1Y = "P1Y"
    P3Y = "P3Y"
    P5Y = "P5Y"
    P10Y = "P10Y"
    P50Y = "P50Y"
    YTD = "YTD"


class ChartRequest(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    callback: str = Field(default="vwd.hchart.seriesRequestManager.sync_response")
    culture: str
    override: dict[str, str] = Field(default_factory=dict)
    format: str = Field(default="json")
    period: Interval
    requestid: str
    resolution: Interval
    series: list[str] = Field(default_factory=list)
    tz: str
    user_token: int | None = Field(default=None)


class Series(BaseModel):
    expires: datetime
    data: list | dict
    id: str
    type: str
    times: str | None = Field(default=None)


class Chart(BaseModel):
    end: str
    requestid: str
    resolution: str
    series: list[Series] = Field(default_factory=list)
    start: str
