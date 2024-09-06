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


class Format(str, Enum):
    CSV = "csv"
    HTML = "html"
    PDF = "pdf"
    XLS = "xls"


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


class UpdateOption(str, Enum):
    ALERTS = "alerts"
    CASH_FUNDS = "cashFunds"
    HISTORICAL_ORDERS = "historicalOrders"
    ORDERS = "orders"
    PORTFOLIO = "portfolio"
    TOTAL_PORTFOLIO = "totalPortfolio"
    TRANSACTIONS = "transactions"


class UpdateRequest(BaseModel):
    option: UpdateOption
    last_updated: int = Field(default=0)


class AccountUpdate(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        extra="allow",
        populate_by_name=True,
    )

    alerts: dict | None = Field(default=None)
    cash_funds: dict | None = Field(default=None)
    historical_orders: dict | None = Field(default=None)
    orders: dict | None = Field(default=None)
    portfolio: dict | None = Field(default=None)
    total_portfolio: dict | None = Field(default=None)
    transactions: dict | None = Field(default=None)

class UpcomingPayments(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        extra="allow",
        populate_by_name=True,
    )

    ca_id: str
    product: str
    description: str
    currency: str
    amount: str
    amount_in_base_curr: str
    pay_date: str