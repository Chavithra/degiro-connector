from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class HistoryRequest(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        json_encoders={date: lambda v: v.strftime("%d/%m/%Y") if v else None},
    )

    from_date: date
    to_date: date
    group_transactions_by_order: bool = Field(default=False)

    int_account: int | None = Field(default=None)
    session_id: str | None = Field(default=None)


class HistoryItem(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        extra="allow",
        populate_by_name=True,
    )

    auto_fx_fee_in_base_currency: float | None = Field(default=None)
    buysell: str | None = Field(default=None)
    counter_party: str | None = Field(default=None)
    date: datetime | None = Field(default=None)
    executing_entity_id: str | None = Field(default=None)
    fee_in_base_currency: float | None = Field(default=None)
    fx_rate: float | None = Field(default=None)
    gross_fx_rate: float | None = Field(default=None)
    id: int | None = Field(default=None)
    nett_fx_rate: float | None = Field(default=None)
    order_type_id: int | None = Field(default=None)
    price: float | None = Field(default=None)
    product_id: int | None = Field(default=None)
    quantity: int | None = Field(default=None)
    total: float | None = Field(default=None)
    total_fees_in_base_currency: float | None = Field(default=None)
    total_in_base_currency: float | None = Field(default=None)
    total_plus_all_fees_in_base_currency: float | None = Field(default=None)
    total_plus_fee_in_base_currency: float | None = Field(default=None)
    transfered: bool | None = Field(default=None)
    trading_venue: str | None = Field(default=None)
    transaction_type_id: int | None = Field(default=None)


class TransactionsHistory(BaseModel):
    data: list[HistoryItem] = Field(default_factory=list)
