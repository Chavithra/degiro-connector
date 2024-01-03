import json
import logging

from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.models.credentials import Credentials

logging.basicConfig(level=logging.DEBUG)

with open("config/config.json") as config_file:
    config_dict = json.load(config_file)

credentials = Credentials.model_validate(obj=config_dict)
trading_api = TradingAPI(credentials=credentials)
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
