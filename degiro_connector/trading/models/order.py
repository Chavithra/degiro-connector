from datetime import date, datetime, timedelta
from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class Action(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderType(int, Enum):
    LIMIT = 0
    MARKET = 2
    STOP_LIMIT = 1
    STOP_LOSS = 3

    # LIMIT_HIT = ?;
    # TRAILING_STOP = ?;
    # JOIN = ?;
    # STANDARD_SIZE = ?;
    # STANDARD_AMOUNT = ?;
    # TAKE_PROFIT = ?;
    # COMBINED = ?;
    # OCO = ?;


class TimeType(int, Enum):
    GOOD_TILL_CANCELED = 3
    GOOD_TILL_DAY = 1
    UNKNOWN_0 = 0
    UNKNOWN_2 = 2


class Order(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    # USED IN CHECKING
    buy_sell: Action | None = Field(default=None)
    id: str | None = Field(default=None)
    order_type: OrderType | None = Field(default=None)
    price: float | None = Field(default=None)
    product_id: int | None = Field(default=None)
    size: float | None = Field(default=None)
    stop_price: float = Field(default=None)
    time_type: TimeType = Field(default=None)

    # USED IN CONFIRMATION
    contract_size: float | None = Field(default=None)
    contract_type: int | None = Field(default=None)
    currency: str | None = Field(default=None)
    date: str | None = Field(
        default=None
    )  # hour : called "date" by the API contains %H:%M if the date was not passed
    is_deletable: bool | None = Field(default=None)
    is_modifiable: bool | None = Field(default=None)
    product: str | None = Field(default=None)
    quantity: float | None = Field(default=None)
    total_order_value: float | None = Field(default=None)

    # USED IN HISTORY
    retained_order: bool | None = Field(alias="retainedOrder", default=None)
    sent_to_exchange: bool | None = Field(alias="sentToExchange", default=None)


class CheckingResponse(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    auto_fx_conversion_rate: float | None = Field(default=None)
    confirmation_id: str
    free_space_new: float | None = Field(default=None)
    response_datetime: datetime | None = Field(default=None)
    request_duration: timedelta | None = Field(default=None)
    transaction_auto_fx_opposite_surcharges: list[dict] | None = Field(default=None)
    transaction_auto_fx_surcharges: list[dict] | None = Field(default=None)
    transaction_fee: float | None = Field(default=None)
    transaction_fees: list[dict] | None = Field(default=None)
    transaction_opposite_fees: list[dict] | None = Field(default=None)
    transaction_taxes: list[dict] | None = Field(default=None)
    show_ex_ante_report_link: bool | None = Field(default=None)


class CheckingWrapper(BaseModel):
    data: CheckingResponse


class ConfirmationResponse(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )
    order_id: str
    response_datetime: datetime | None = Field(default=None)
    request_duration: timedelta | None = Field(default=None)


class ConfirmationWrapper(BaseModel):
    data: ConfirmationResponse


ORDER_FIELD_MAP = {
    OrderType.LIMIT: {
        "buySell",
        "orderType",
        "price",
        "productId",
        "size",
        "timeType",
    },
    OrderType.STOP_LIMIT: {
        "buySell",
        "orderType",
        "price",
        "productId",
        "size",
        "stopPrice",
        "timeType",
    },
    OrderType.MARKET: {
        "buySell",
        "orderType",
        "productId",
        "size",
        "timeType",
    },
    OrderType.STOP_LOSS: {
        "buySell",
        "orderType",
        "productId",
        "size",
        "stopPrice",
        "timeType",
    },
}


class HistoryItem(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    buysell: Literal["B", "S"]
    created: datetime
    current_traded_size: int
    active: bool
    last: datetime
    order_id: str | None = Field(default=None)
    order_time_type_id: TimeType
    order_type_id: OrderType
    price: float
    product_id: int
    size: int
    status: str
    stop_price: float
    total_traded_size: int
    type: str


class History(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    data: list[HistoryItem] = Field(default_factory=list)


class HistoryRequest(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        json_encoders={date: lambda v: v.strftime("%d/%m/%Y") if v else None},
    )

    from_date: date
    to_date: date

    int_account: int | None = Field(default=None)
    session_id: str | None = Field(default=None)
