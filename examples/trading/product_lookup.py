import json
import logging
import degiro_connector.core.helpers.pb_handler as payload_handler

from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.models.credentials import Credentials
from degiro_connector.trading.models.trading_pb2 import ProductSearch

logging.basicConfig(level=logging.DEBUG)

with open("config/config.json") as config_file:
    config_dict = json.load(config_file)

credentials = Credentials.model_validate(obj=config_dict)

# SETUP TRADING API
trading_api = TradingAPI(credentials=credentials)

# ESTABLISH CONNECTION
trading_api.connect()

# SETUP REQUEST
request_lookup = ProductSearch.RequestLookup(
    search_text="APPLE",
    limit=2,
    offset=0,
    product_type_id=1,
)

# FETCH DATA
products_lookup = trading_api.product_search(request=request_lookup, raw=False)
products_lookup_dict = payload_handler.message_to_dict(message=products_lookup)
pretty_json = json.dumps(products_lookup_dict, sort_keys=True, indent=4)

print(pretty_json)
