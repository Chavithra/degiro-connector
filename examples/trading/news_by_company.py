import json
import logging

from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.models.credentials import Credentials
from degiro_connector.trading.models.news import NewsRequest

logging.basicConfig(level=logging.DEBUG)

with open("config/config.json") as config_file:
    config_dict = json.load(config_file)

credentials = Credentials.model_validate(obj=config_dict)

# SETUP TRADING API
trading_api = TradingAPI(credentials=credentials)

# CONNECT
trading_api.connect()

# SETUP REQUEST
news_request = NewsRequest(
    isin="NL0000235190",
    limit=10,
    offset=0,
    languages="en,fr",
)

# FETCH DATA
company_news = trading_api.get_news_by_company(news_request=news_request, raw=False)

print("Here are the company news :", company_news)
