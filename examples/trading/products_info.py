import json
import logging

from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.models.credentials import Credentials
from degiro_connector.trading.models.trading_pb2 import (
    ProductsInfo,
)

logging.basicConfig(level=logging.DEBUG)

with open("config/config.json") as config_file:
    config_dict = json.load(config_file)

credentials = Credentials.model_validate(obj=config_dict)

# SETUP TRADING API
trading_api = TradingAPI(credentials=credentials)

# CONNECT
trading_api.connect()

# SETUP REQUEST
request = ProductsInfo.Request()
request.products.extend([96008, 1153605, 5462588])

# FETCH DATA
products_info = trading_api.get_products_info(
    request=request,
    raw=True,
)

# DISPLAY PRODUCTS_INFO
print(products_info)
