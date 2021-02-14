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
favourites_list = trading_api.get_favourites_list(raw=False)

# DISPLAY - MESSAGE
for list in favourites_list.values:
    print('id:', list.id)
    print('name:', list.name)
    print('is_default:', list.is_default)
    print('product_ids:', list.product_ids)
    print('-')

# FETCH DATA - DICT
favourites_list_dict = trading_api.get_favourites_list(raw=True)

# DISPLAY - DICT
print(favourites_list_dict)
