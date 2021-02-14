# IMPORTATIONS
import datetime
import json
import logging

from trading.api import API as TradingAPI
from trading.pb.trading_pb2 import (
    Credentials,
    OrdersHistory,
)

# SETUP LOGGING LEVEL
logging.basicConfig(level=logging.DEBUG)

# SETUP CONFIG DICT
with open('config/config.json') as config_file:
    config_dict = json.load(config_file)

# SETUP CREDENTIALS
int_account = config_dict['int_account']
username = config_dict['username']
password = config_dict['password']
credentials = Credentials(
    int_account=int_account,
    username=username,
    password=password,
)

# SETUP TRADING API
trading_api = TradingAPI(credentials=credentials)

# CONNECT
trading_api.connect()

# SETUP REQUEST
today = datetime.date.today()
from_date = OrdersHistory.Request.Date(
    year=2020,
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
