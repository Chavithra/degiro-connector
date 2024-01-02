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

    auto_fx_fee_in_base_currency: float | None
    buysell: str | None
    counter_party: str | None
    date: datetime | None
    executing_entity_id: str | None
    fee_in_base_currency: float | None
    fx_rate: float | None
    gross_fx_rate: float | None
    id: int | None
    nett_fx_rate: float | None
    order_type_id: int | None
    price: float | None
    product_id: int | None
    quantity: int | None
    total: float | None
    total_fees_in_base_currency: float | None
    total_in_base_currency: float | None
    total_plus_all_fees_in_base_currency: float | None
    total_plus_fee_in_base_currency: float | None
    transfered: bool | None
    trading_venue: str | None
    transaction_type_id: int | None


class TransactionsHistory(BaseModel):
    data: list[HistoryItem] = Field(default_factory=list)
