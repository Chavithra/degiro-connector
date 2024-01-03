import json
import logging

from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.models.credentials import Credentials
from degiro_connector.trading.models.product_search import LookupRequest


logging.basicConfig(level=logging.DEBUG)

with open("config/config.json") as config_file:
    config_dict = json.load(config_file)

credentials = Credentials.model_validate(obj=config_dict)
trading_api = TradingAPI(credentials=credentials)
trading_api.connect()

# FETCH PRODUCTS
lookup_request = LookupRequest(
    search_text="APPLE",
    limit=2,
    offset=0,
    product_type_id=1,
)

product_batch = trading_api.product_search(product_request=lookup_request, raw=False)

print(product_batch)
