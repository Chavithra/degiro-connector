import datetime
import json
import logging

from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.models.credentials import Credentials
from degiro_connector.trading.models.trading_pb2 import (
    OrdersHistory,
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
today = datetime.date.today()
from_date = OrdersHistory.Request.Date(
    year=today.year,
    month=10,
    day=1,
)
to_date = OrdersHistory.Request.Date(
    year=today.year,
    month=today.month,
    day=today.day,
)
request = OrdersHistory.Request(
    from_date=from_date,
    to_date=to_date,
)

# FETCH DATA
orders_history = trading_api.get_orders_history(
    request=request,
    raw=False,
)

# DISPLAY TRANSACTIONS
for order in orders_history.values:
    print(dict(order))
