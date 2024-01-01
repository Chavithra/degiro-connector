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

# UPDATE A FAVORITE LIST NAME
id = 1234567
name = "SOME_OTHER_NAME"
success = trading_api.update_favorite_list(id=id, name=name)

# DISPLAY - MESSAGE
if success:
    print(f"The following list was update : {name} = {id}.")
else:
    print(f"Can't update this list : {name} =  = {id}.")
