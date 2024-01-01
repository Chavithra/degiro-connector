import json
import logging

from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.models.credentials import Credentials

logging.basicConfig(level=logging.DEBUG)

with open("config/config.json") as config_file:
    config_dict = json.load(config_file)

credentials = Credentials(
    int_account=None,
    username=username,
    password=password,
    totp_secret_key=totp_secret_key,
    one_time_password=one_time_password,
)

# SETUP TRADING API
trading_api = TradingAPI(credentials=credentials)

# CONNECT
trading_api.connect()

# FETCH CONFIG TABLE
config_table = trading_api.get_config()

# EXTRACT DATA
user_token = config_table["clientId"]
session_id = config_table["sessionId"]

# DISPLAY DATA
config_pretty = json.dumps(config_table, sort_keys=True, indent=4)

print('Your "user_token" is :', user_token)
print("Here is the rest of config :", config_pretty)
