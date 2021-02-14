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
client_details_table = trading_api.get_client_details()

# EXTRACT DATA
int_account = client_details_table['data']['intAccount']
user_token = client_details_table['data']['id']
client_details_pretty = json.dumps(
    client_details_table,
    sort_keys=True,
    indent=4,
)

# DISPLAY DATA
print('Your "int_account" is :', int_account)
print('Your "user_token" is :', user_token)
print('Here is the rest your details :', client_details_pretty)
