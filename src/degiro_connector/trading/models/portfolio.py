from datetime import date as Date
from enum import Enum

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class Period(str, Enum):
    ONE_MONTH = "1M"
    THREE_MONTHS = "3M"
    YTD = "YTD"
    ONE_YEAR = "1Y"


class PortfolioValueRequest(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        validate_by_name=True,
    )

    period: Period


class PortfolioValue(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        extra="allow",
        validate_by_name=True,
    )

    date: Date
    value: float
