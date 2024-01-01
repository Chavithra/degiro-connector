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

# FETCH DATA - MESSAGE
products_config = trading_api.get_products_config(raw=False)

# DISPLAY - MESSAGE
for item in products_config.values:
    print(item)

# FETCH DATA - DICT
products_config_dict = trading_api.get_products_config(raw=True)
products_config_pretty = json.dumps(
    products_config_dict,
    sort_keys=True,
    indent=4,
)

# DISPLAY - DICT
print(products_config_pretty)
