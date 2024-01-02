from datetime import datetime, date
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class OverviewRequest(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        json_encoders={date: lambda v: v.strftime("%d/%m/%Y") if v else None},
    )

    from_date: date
    to_date: date


class CashMovements(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    balance: dict | None = Field(default=None)
    change: float | None = Field(default=None)
    currency: str | None = Field(default=None)
    date: datetime | None = Field(default=None)
    description: str | None = Field(default=None)
    id: int | None = Field(default=None)
    product_id: int | None = Field(default=None)
    type: str | None = Field(default=None)
    value_date: datetime | None = Field(default=None)


class AccountOverview(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )
    cash_movements: list[CashMovements] | None = Field(default=None)


class OverviewWrapper(BaseModel):
    data: AccountOverview


class Format(int, Enum):
    CSV = "csv"
    HTML = "html"
    PDF = "pdf"
    XLS = "xml"


class ReportRequest(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        json_encoders={date: lambda v: v.strftime("%d/%m/%Y") if v else None},
    )

    country: str
    lang: str
    format: Format = Field(default=Format.CSV)
    from_date: date
    to_date: date

    int_account: int | None = Field(default=None)
    session_id: str | None = Field(default=None)


class Report(BaseModel):
    content: str
    format: Format
