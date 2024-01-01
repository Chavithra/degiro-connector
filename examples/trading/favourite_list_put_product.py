import json
import logging

from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.models.credentials import Credentials

logging.basicConfig(level=logging.DEBUG)

with open("config/config.json") as config_file:
    config_dict = json.load(config_file)

credentials = Credentials.model_validate(obj=config_dict)
trading_api = TradingAPI(credentials=credentials)
trading_api.connect()

# DELETE AN EXISTING FAVORITE LIST
product_id = 65009
list_id = 2608650
success = trading_api.put_favorite_list_product(list_id=list_id, product_id=product_id)

if success:
    print(f"The following product was added : {product_id} => {list_id}")
else:
    print(f"Can't add the following product : {product_id} => {list_id}")
