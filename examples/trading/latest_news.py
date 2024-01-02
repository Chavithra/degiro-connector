import json
import logging

from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.models.credentials import Credentials
from degiro_connector.trading.models.news import LatestRequest

logging.basicConfig(level=logging.DEBUG)

with open("config/config.json") as config_file:
    config_dict = json.load(config_file)

credentials = Credentials.model_validate(obj=config_dict)
trading_api = TradingAPI(credentials=credentials)
trading_api.connect()

# FETCH LATEST NEWS
latest_request = LatestRequest(
    offset=0,
    languages="en,fr",
    limit=20,
)
latest_news = trading_api.get_latest_news(latest_request=latest_request, raw=False)

print("Here are the latest news :", latest_news)
