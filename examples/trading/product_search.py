# IMPORTATIONS
import json
import logging

from trading.api import API as TradingAPI
from trading.pb.trading_pb2 import Credentials, ProductSearch

# SETUP LOGGING LEVEL
logging.basicConfig(level=logging.DEBUG)

# SETUP CONFIG DICT
with open('config/config.json') as config_file:
    config_dict = json.load(config_file)

# SETUP CREDENTIALS
int_account = config_dict['int_account']
username = config_dict['username']
password = config_dict['password']
credentials = Credentials(
    int_account=int_account,
    username=username,
    password=password,
)

# SETUP TRADING API
trading_api = TradingAPI(credentials=credentials)

# ESTABLISH CONNECTION
trading_api.connect()

# SETUP REQUEST
request_stock = ProductSearch.RequestStocks(
    index_id=5,
    is_in_us_green_list=False,
    stock_country_id=886,
    offset=0,
    limit=100,
    require_total=True,
    sort_columns='name',
    sort_types='asc',
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
