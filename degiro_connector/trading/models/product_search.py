from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator
from pydantic.alias_generators import to_camel


class ProductInfo(BaseModel):
    model_config = ConfigDict(
        extra="allow",
        alias_generator=to_camel,
        populate_by_name=True,
    )


class ProductsConfig(ProductInfo):
    values: dict


class BondsRequest(ProductInfo):
    bond_issuer_type_id: int
    bond_exchange_id: int
    search_text: str
    offset: int
    limit: int
    require_total: bool
    sort_columns: str
    sort_types: str


class ETFsRequest(ProductInfo):
    popular_only: bool
    input_aggregate_types: str
    input_aggregate_values: str
    search_text: str
    offset: int
    limit: int
    require_total: bool
    sort_columns: str
    sort_types: str


class FundsRequest(ProductInfo):
    search_text: str
    offset: int
    limit: int
    require_total: bool
    sort_columns: str
    sort_types: str


class FuturesRequest(ProductInfo):
    future_exchange_id: int
    underlying_isin: str
    search_text: str
    offset: int
    limit: int
    require_total: bool
    sort_columns: str
    sort_types: str


class LeveragedsRequest(ProductInfo):
    popular_only: bool
    input_aggregate_types: str
    input_aggregate_values: str
    search_text: str
    offset: int
    limit: int
    require_total: bool
    sort_columns: str
    sort_types: str
    underlying_product_id: int | None = Field(default=None)
    shortlong: str | None = Field(default=None)


class LookupRequest(ProductInfo):
    search_text: str
    limit: int = Field(default=5)
    offset: int = Field(default=0)
    product_type_id: int | None = Field(default=None)


class OptionsRequest(ProductInfo):
    input_aggregate_types: str
    input_aggregate_values: str
    option_exchange_id: int
    underlying_isin: str
    search_text: str
    offset: int
    limit: int
    require_total: bool
    sort_columns: str
    sort_types: str


class StocksRequest(ProductInfo):
    exchange_id: int | None = Field(default=None)
    is_in_us_green_list: bool | None = Field(default=None, alias="isInUSGreenList")
    index_id: int | None = Field(default=None)
    offset: int = Field(default=10)
    limit: int = Field(default=0)
    require_total: bool = Field(default=False)
    search_text: str | None = Field(default=None)
    sort_columns: str = Field(default="name")
    sort_types: str = Field(default="asc")
    stock_country_id: int | None = Field(default=None)


class WarrantsRequest(ProductInfo):
    search_text: str
    offset: int
    limit: int
    require_total: bool
    sort_columns: str
    sort_types: str


class ProductBatch(BaseModel):
    offset: int
    products: list[dict] | None = Field(default=None)
    response_datetime: datetime = Field(default_factory=datetime.now)
    total: int = Field(default=0)


class UnderlyingsRequest(ProductInfo):
    future_exchange_id: int | None = Field(default=None)
    option_exchange_id: int | None = Field(default=None)

    int_account: int | None = Field(default=None)
    session_id: str | None = Field(default=None)

    @model_validator(mode="before")
    @classmethod
    def one_of(cls, data: Any):
        if isinstance(data, dict):
            if "future_exchange_id" in data and "option_exchange_id" in data:
                raise ValueError(
                    "Can't set both: `future_exchange_id` and `option_exchange_id`."
                )
            if "future_exchange_id" not in data and "option_exchange_id" not in data:
                raise ValueError(
                    "One of these parameters should be set: `future_exchange_id` or `option_exchange_id`."
                )

        return data


class Underlying(ProductInfo):
    contract_type: int | None = Field(default=None)
    isin: str | None = Field(default=None)
    name: str | None = Field(default=None)
    symbol: str | None = Field(default=None)
    underlying_name: str | None = Field(default=None)
    underlying_product_id: int | None = Field(default=None)
