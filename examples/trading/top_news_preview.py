import json
import logging

from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.models.credentials import Credentials
from degiro_connector.trading.models.news import PreviewRequest

logging.basicConfig(level=logging.DEBUG)

with open("config/config.json") as config_file:
    config_dict = json.load(config_file)

credentials = Credentials.model_validate(obj=config_dict)
trading_api = TradingAPI(credentials=credentials)
trading_api.connect()

# FETCH DATA
preview_request = PreviewRequest(
    limit=20,
    category="FixedIncome",
)
top_news_preview = trading_api.get_top_news_preview(
    preview_request=preview_request, raw=False
)

print(top_news_preview)
