from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class CalendarType(str, Enum):
    DIVIDEND_CALENDAR = "DividendCalendar"
    ECONOMIC_CALENDAR = "EconomicCalendar"
    EARNINGS_CALENDAR = "EarningsCalendar"
    HOLIDAY_CALENDAR = "HolidayCalendar"
    IPO_CALENDAR = "IpoCalendar"
    SPLIT_CALENDAR = "SplitCalendar"


class AgendaRequest(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        extra="allow",
        populate_by_name=True,
        json_encoders={
            datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%SZ") if v else None
        },
    )

    calendar_type: CalendarType
    classifications: str | None = Field(default=None)
    company_name: str | None = Field(default=None)
    countries: str | None = Field(default=None)
    end_date: datetime
    limit: int = Field(default=25)
    offset: int = Field(default=0)
    sort_column: str | None = Field(default="date")
    sort_type: str | None = Field(default="asc")
    start_date: datetime
    units: str | None = Field(default=None)

    int_account: int | None = Field(default=None)
    session_id: str | None = Field(default=None)


class Agenda(BaseModel):
    items: list[dict]
    offset: int
    total: int
