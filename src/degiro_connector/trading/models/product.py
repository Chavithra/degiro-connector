from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class ProductItem(BaseModel):
    model_config = ConfigDict(
        extra="allow",
        alias_generator=to_camel,
        populate_by_name=True,
    )

    active: bool | None = Field(default=None)
    buy_order_types: list[str] | None = Field(default=None)
    category: str | None = Field(default=None)
    close_price: float | None = Field(default=None)
    close_price_date: str | None = Field(default=None)
    contract_size: int | None = Field(default=None)
    currency: str | None = Field(default=None)
    exchange_id: str | None = Field(default=None)
    feed_quality: str | None = Field(default=None)
    feed_quality_secondary: str | None = Field(default=None)
    id: str | None = Field(default=None)
    is_shortable: bool | None = Field(default=None)
    isin: str | None = Field(default=None)
    name: str | None = Field(default=None)
    only_eod_prices: bool | None = Field(default=None)
    order_book_depth: int | None = Field(default=None)
    order_book_depth_secondary: int | None = Field(default=None)
    order_time_types: list[str] | None = Field(default=None)
    product_bit_types: list[str] | None = Field(default=None)
    product_type: str | None = Field(default=None)
    product_type_id: int | None = Field(default=None)
    quality_switch_free: bool | None = Field(default=None)
    quality_switch_free_secondary: bool | None = Field(default=None)
    quality_switchable: bool | None = Field(default=None)
    quality_switchable_secondary: bool | None = Field(default=None)
    sell_order_types: list[str] | None = Field(default=None)
    strike_price: float | None = Field(default=None)
    symbol: str | None = Field(default=None)
    tradable: bool | None = Field(default=None)
    vwd_id: str | None = Field(default=None)
    vwd_id_secondary: str | None = Field(default=None)
    vwd_identifier_type: str | None = Field(default=None)
    vwd_identifier_type_secondary: str | None = Field(default=None)
    vwd_module_id: int | None = Field(default=None)
    vwd_module_id_secondary: int | None = Field(default=None)


class ProductInfo(BaseModel):
    data: dict[int, ProductItem] = Field(default_factory=dict)


class FinancialStatements(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        extra="allow",
        populate_by_name=True,
    )

    annual: list[dict] = Field(default_factory=list)
    currency: str | None = Field(default=None)
    interim: list[dict] = Field(default_factory=list)


class StatementsWrapper(BaseModel):
    data: FinancialStatements


class EstimatesSummaries(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        extra="allow",
        populate_by_name=True,
    )
    annual: list[dict] = Field(default_factory=list)
    interim: list[dict] = Field(default_factory=list)
    ric: str | None = Field(default=None)
    currency: str | None = Field(default=None)
    lastUpdated: datetime | None = Field(default=None)
    lastRetrieved: datetime | None = Field(default=None)
    preferredMeasure: str | None = Field(default=None)


class SummariesWrapper(BaseModel):
    data: EstimatesSummaries
