# IMPORTATIONS
import json
import logging

from trading.api import API as TradingAPI
from trading.pb.trading_pb2 import Credentials

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

# CONNECT
trading_api.connect()

# FETCH DATA - MESSAGE
products_config = trading_api.get_products_config(raw=False)

# DISPLAY - MESSAGE
for item in products_config.values:
    print(item)

# FETCH DATA - DICT
products_config_dict = trading_api.get_products_config(raw=True)

# DISPLAY - DICT
print(products_config_dict)
