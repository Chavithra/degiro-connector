# IMPORTATIONS
import json
import logging

from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.models.trading_pb2 import Credentials

# SETUP LOGGING LEVEL
logging.basicConfig(level=logging.DEBUG)

# SETUP CONFIG DICT
with open("config/config.json") as config_file:
    config_dict = json.load(config_file)

# SETUP CREDENTIALS
int_account = config_dict.get("int_account")
username = config_dict.get("username")
password = config_dict.get("password")
totp_secret_key = config_dict.get("totp_secret_key")
one_time_password = config_dict.get("one_time_password")

credentials = Credentials(
    int_account=int_account,
    username=username,
    password=password,
    totp_secret_key=totp_secret_key,
    one_time_password=one_time_password,
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
products_config_pretty = json.dumps(
    products_config_dict,
    sort_keys=True,
    indent=4,
)

# DISPLAY - DICT
print(products_config_pretty)
