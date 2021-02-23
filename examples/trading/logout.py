# IMPORTATIONS
import json
import logging
import random
import time

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

# ACCESS SESSION_ID
session_id = trading_api.connection_storage.session_id

# Waiting
sleep_time = random.uniform(1, 5)
print(f'Waiting : {sleep_time}s ')
time.sleep(sleep_time)

# FETCH CONFIG TABLE
print(len(trading_api.get_config()))

# LOGOUT
print('Logout, session id : ', session_id)
trading_api.logout()

try:
    # FETCH CONFIG TABLE
    print(len(trading_api.get_config()))
except ConnectionError as e:
    print(e)
    print('Logout : success !')
else:
    print('Logout : fail !')
