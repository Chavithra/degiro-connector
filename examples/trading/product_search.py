# IMPORTATIONS
import json
import logging

from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.models.trading_pb2 import Credentials, ProductSearch

# SETUP LOGGING LEVEL
logging.basicConfig(level=logging.DEBUG)

# SETUP CONFIG DICT
with open("config/config.json") as config_file:
    config_dict = json.load(config_file)

# SETUP CREDENTIALS
int_account = config_dict.get("int_account")
username = config_dict.get("username")
password = config_dict.get("password")
totp_secret_key = config_dict.get("totp_secret_key")
one_time_password = config_dict.get("one_time_password")

credentials = Credentials(
    int_account=int_account,
    username=username,
    password=password,
    totp_secret_key=totp_secret_key,
    one_time_password=one_time_password,
)

# SETUP TRADING API
trading_api = TradingAPI(credentials=credentials)

# ESTABLISH CONNECTION
trading_api.connect()

# SETUP REQUEST
request_stock = ProductSearch.RequestStocks(
    index_id=122001,  # NASDAQ 100
    exchange_id=663,  # NASDAQ
    # You can either use `index_id` or `exchange id`
    # See which one to use in the `ProductsConfig` table
    is_in_us_green_list=True,
    stock_country_id=846,  # US
    offset=0,
    limit=100,
    require_total=True,
    sort_columns="name",
    sort_types="asc",
)

# FETCH DATA
stock_list = trading_api.product_search(request=request_stock, raw=False)

# LOOP OVER PRODUCTS
for product in stock_list.products:
    print(dict(product))

# LOOP OVER COLUMNS
product = stock_list.products[0]
for column in product:
    print(column, product[column])
