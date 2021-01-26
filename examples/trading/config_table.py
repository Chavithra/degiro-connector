# IMPORTATIONS
import json

from trading.api import API as TradingAPI
from trading.pb.trading_pb2 import Credentials

# SETUP CONFIG DICT
with open('config/config.json') as config_file:
    config_dict = json.load(config_file)

# SETUP CREDENTIALS
int_account = config_dict['int_account']
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
config_pretty = json.dumps(config_table, sort_keys=True, indent=4)

# DISPLAY DATA
print('Your "user_token" is :', user_token)
print('Here is the rest of config :', config_pretty)