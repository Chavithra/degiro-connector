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

# CREATE A FAVORITE LIST
name = "SOME_LIST"
favourite_list_id = trading_api.create_favourite_list(name=name)

if favourite_list_id:
    print(f"The following list was created : {name} = {favourite_list_id}.")
else:
    print(f"Can't create this list : {name}.")
