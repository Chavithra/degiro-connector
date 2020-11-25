# IMPORTATIONS
import json
import logging
import quotecast.helpers.pb_handler as pb_handler

from IPython.display import display
from trading.api import API as TradingAPI
from trading.pb.trading_pb2 import Credentials, ProductsLookup

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
trading_api.connection_storage.connect()

# FETCH DATA
request = ProductsLookup.Request(
    search_text='APPLE',
    limit=10,
    offset=0,
)
products_lookup = trading_api.products_lookup(request=request)

# LOOP OVER PRODUCTS
for product in products_lookup.products:
    print('id:', product['id'])
    print('name:', product['name'])
    print('productType:', product['productType'])
    print('symbol:', product['symbol'])
    print('vwdId:', dict(product).get('vwdId', 'unknown'))
    print('-')

# LOOP OVER COLUMNS
product = products_lookup.products[0]
for column in product:
    print(column, product[column])