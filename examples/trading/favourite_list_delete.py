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
list_id = 1234567
success = trading_api.delete_favorite_list(list_id=list_id)

if success:
    print(f"The following list was deleted : {list_id}.")
else:
    print(f"Can't delete this list : {list_id}.")
