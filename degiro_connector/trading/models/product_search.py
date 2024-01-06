from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class ProductRequest(BaseModel):
    model_config = ConfigDict(
        extra="allow",
        alias_generator=to_camel,
        populate_by_name=True,
    )


class ProductsConfig(ProductRequest):
    values: dict


class BondsRequest(ProductRequest):
    bond_issuer_type_id: int
    bond_exchange_id: int
    search_text: str
    offset: int
    limit: int
    require_total: bool
    sort_columns: str
    sort_types: str


class ETFsRequest(ProductRequest):
    popular_only: bool
    input_aggregate_types: str
    input_aggregate_values: str
    search_text: str
    offset: int
    limit: int
    require_total: bool
    sort_columns: str
    sort_types: str


class FundsRequest(ProductRequest):
    search_text: str
    offset: int
    limit: int
    require_total: bool
    sort_columns: str
    sort_types: str


class FuturesRequest(ProductRequest):
    future_exchange_id: int
    underlying_isin: str
    search_text: str
    offset: int
    limit: int
    require_total: bool
    sort_columns: str
    sort_types: str


class LeveragedsRequest(ProductRequest):
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


class LookupRequest(ProductRequest):
    search_text: str
    limit: int = Field(default=5)
    offset: int = Field(default=0)
    product_type_id: int


class OptionsRequest(ProductRequest):
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


class StocksRequest(ProductRequest):
    exchange_id: int | None = Field(default=None)
    is_in_us_green_list: bool | None = Field(default=None, alias="isInUSGreenList")
    index_id: int | None = Field(default=None)
    offset: int = Field(default=10)
    limit: int = Field(default=0)
    require_total: bool = Field(default=False)
    search_text: str | None = Field(default=None)
    sort_columns: str
    sort_types: str
    stock_country_id: int


class WarrantsRequest(ProductRequest):
    search_text: str
    offset: int
    limit: int
    require_total: bool
    sort_columns: str
    sort_types: str


class ProductBatch(BaseModel):
    offset: int
    products: list[dict]
    response_datetime: datetime = Field(default_factory=datetime.now)
    total: int = Field(default=0)
