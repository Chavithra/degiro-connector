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
totp_secret_key = config_dict['totp_secret_key']

credentials = Credentials(
    int_account=None,
    username=username,
    password=password,
    totp_secret_key=totp_secret_key,
)

# SETUP TRADING API
trading_api = TradingAPI(credentials=credentials)

# CONNECT
trading_api.connect()

# ACCESS SESSION_ID
session_id = trading_api.connection_storage.session_id

print('You are now connected, with the session id :', session_id)
