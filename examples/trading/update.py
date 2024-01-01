import json
import logging
import degiro_connector.core.helpers.pb_handler as pb_handler

# from IPython.display import display
from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.models.credentials import Credentials
from degiro_connector.trading.models.trading_pb2 import Update

logging.basicConfig(level=logging.DEBUG)

with open("config/config.json") as config_file:
    config_dict = json.load(config_file)

credentials = Credentials.model_validate(obj=config_dict)

trading_api = TradingAPI(credentials=credentials)
trading_api.connect()
request_list = Update.RequestList()
request_list.values.extend(
    [
        Update.Request(option=Update.Option.ORDERS, last_updated=0),
        Update.Request(option=Update.Option.PORTFOLIO, last_updated=0),
        Update.Request(option=Update.Option.TOTALPORTFOLIO, last_updated=0),
    ]
)

# FETCH DATA
update = trading_api.get_update(request_list=request_list, raw=False)
update_dict = pb_handler.message_to_dict(message=update)

print(update_dict)
