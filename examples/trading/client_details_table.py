import json
import quotecast.helpers.pb_handler as pb_handler
import pandas as pd

from IPython.display import display
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
    int_account=int_account,
    username=username,
    password=password,
)

# SETUP TRADING API
trading_api = TradingAPI(credentials=credentials)

# CONNECT
trading_api.connection_storage.connect()

# FETCH CONFIG TABLE
client_details_table = trading_api.get_client_details()

print(client_details_table)