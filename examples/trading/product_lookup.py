# IMPORTATIONS
import json
import logging
import trading.helpers.payload_handler as payload_handler

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
request_lookup = ProductSearch.RequestLookup(
    search_text='APPLE',
    limit=2,
    offset=0,
)

# FETCH DATA
products_lookup = trading_api.product_search(request=request_lookup, raw=False)
products_lookup_dict = payload_handler.message_to_dict(message=products_lookup)
pretty_json = json.dumps(products_lookup_dict, sort_keys=True, indent=4)

print(pretty_json)
