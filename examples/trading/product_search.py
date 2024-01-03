import json
import logging

import polars as pl

from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.models.credentials import Credentials
from degiro_connector.trading.models.product_search import StocksRequest

logging.basicConfig(level=logging.DEBUG)

with open("config/config.json") as config_file:
    config_dict = json.load(config_file)

credentials = Credentials.model_validate(obj=config_dict)

trading_api = TradingAPI(credentials=credentials)
trading_api.connect()

# FETCH PRODUCTS
request_stock = StocksRequest(
    index_id=122001,  # NASDAQ 100
    # exchange_id=663,  # NASDAQ
    # You can either use `index_id` or `exchange id`
    # See which one to use in the `ProductsConfig` table
    is_in_us_green_list=True,  # type: ignore
    stock_country_id=846,  # US
    offset=0,
    limit=100,
    require_total=True,
    sort_columns="name",
    sort_types="asc",
)
product_search = trading_api.product_search(product_request=request_stock, raw=False)

products_df = pl.DataFrame(product_search.products)
print(products_df)
