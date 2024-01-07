import json
import logging

from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.models.credentials import Credentials
from degiro_connector.trading.models.product_search import UnderlyingsRequest

logging.basicConfig(level=logging.DEBUG)

with open("config/config.json") as config_file:
    config_dict = json.load(config_file)

credentials = Credentials.model_validate(obj=config_dict)
trading_api = TradingAPI(credentials=credentials)
trading_api.connect()

# FETCH UNDERLYINGS
underlying_list = trading_api.get_underlyings(
    underlyings_request= UnderlyingsRequest(
        future_exchange_id=1,
        # option_exchange_id=3,
    ),
    raw=False,
)

print(underlying_list)
