import json
import logging

from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.models.credentials import Credentials

logging.basicConfig(level=logging.DEBUG)

with open("config/config.json") as config_file:
    config_dict = json.load(config_file)

credentials = Credentials.model_validate(obj=config_dict)

# SETUP TRADING API
trading_api = TradingAPI(credentials=credentials)

# CONNECT
trading_api.connect()

# FETCH DATA
top_news_preview = trading_api.get_top_news_preview(raw=True)

# DISPLAY DATA
config_pretty = json.dumps(top_news_preview, sort_keys=True, indent=4)

print("Here is the top news preview :", config_pretty)
