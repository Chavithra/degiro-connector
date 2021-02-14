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
username = config_dict['username']
password = config_dict['password']

credentials = Credentials(
    int_account=None,
    username=username,
    password=password,
)

# SETUP TRADING API
trading_api = TradingAPI(credentials=credentials)

# CONNECT
trading_api.connect()

# FETCH CONFIG TABLE
config_table = trading_api.get_config()

# EXTRACT DATA
user_token = config_table['clientId']
session_id = config_table['sessionId']

# DISPLAY DATA
config_pretty = json.dumps(config_table, sort_keys=True, indent=4)

print('Your "user_token" is :', user_token)
print('Here is the rest of config :', config_pretty)
