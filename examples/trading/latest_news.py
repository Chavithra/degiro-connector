import json
import logging

from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.models.credentials import Credentials
from degiro_connector.trading.models.trading_pb2 import LatestNews

logging.basicConfig(level=logging.DEBUG)

with open("config/config.json") as config_file:
    config_dict = json.load(config_file)

credentials = Credentials.model_validate(obj=config_dict)

# SETUP TRADING API
trading_api = TradingAPI(credentials=credentials)

# CONNECT
trading_api.connect()

# SETUP REQUEST
request = LatestNews.Request(
    offset=0,
    languages="en,fr",
    limit=20,
)

# FETCH DATA
latest_news = trading_api.get_latest_news(request=request, raw=True)

# DISPLAY DATA
config_pretty = json.dumps(latest_news, sort_keys=True, indent=4)

print("Here are the latest news :", config_pretty)
