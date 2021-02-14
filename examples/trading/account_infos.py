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

# FETCH DATA
account_info_table = trading_api.get_account_info()

# DISPLAY DATA
account_info_pretty = json.dumps(account_info_table, sort_keys=True, indent=4)
print(account_info_pretty)
