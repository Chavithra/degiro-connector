from enum import Enum
from typing import List, Dict

from pydantic import BaseModel, Field


class Interval(int, Enum):
    PT1S = 0
    PT15S = 1
    PT30S = 2
    PT1M = 3
    PT5M = 4
    PT15M = 5
    PT30M = 6
    PT60M = 7
    PT1H = 8
    P1D = 9
    P1W = 10
    P1M = 11
    P3M = 12
    P6M = 13
    P1Y = 14
    P3Y = 15
    P5Y = 16
    P10Y = 17
    P50Y = 18
    YTD = 19


class ChartRequest(BaseModel):
    culture: str
    override: Dict[str, str] = Field(default_factory=dict)
    period: Interval
    requestid: str
    resolution: Interval
    series: List[str] = Field(default_factory=list)
    tz: str


class ChartSerie(BaseModel):
    data: list[list[float]] = Field(default_factory=list)
    expires: str
    id: str
    times: str | None = Field(default=None)
    type: str


class Chart(BaseModel):
    end: str
    requestid: str
    resolution: str
    series: List[ChartSerie] = Field(default_factory=list)
    start: str
