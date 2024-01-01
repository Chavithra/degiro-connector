import json
import logging
import degiro_connector.core.helpers.pb_handler as pb_handler
import pandas as pd

from IPython.display import display
from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.models.credentials import Credentials
from degiro_connector.trading.models.trading_pb2 import Update

logging.basicConfig(level=logging.DEBUG)

with open("config/config.json") as config_file:
    config_dict = json.load(config_file)

credentials = Credentials.model_validate(obj=config_dict)

# SETUP TRADING API
trading_api = TradingAPI(credentials=credentials)

# CONNECT
trading_api.connect()

# SETUP REQUEST
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

# DISPLAY DATA
if "orders" in update_dict:
    orders_df = pd.DataFrame(update_dict["orders"]["values"])
    print("orders")
    display(orders_df)

if "portfolio" in update_dict:
    portfolio_df = pd.DataFrame(update_dict["portfolio"]["values"])
    print("portfolio")
    display(portfolio_df)

if "total_portfolio" in update_dict:
    total_portfolio_df = pd.DataFrame(update_dict["total_portfolio"]["values"])
    print("total_portfolio")
    display(total_portfolio_df)
