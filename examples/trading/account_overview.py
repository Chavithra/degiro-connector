# IMPORTATIONS
import datetime
import json
import logging

from trading.api import API as TradingAPI
from trading.pb.trading_pb2 import (
    AccountOverview,
    Credentials,
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
from_date = AccountOverview.Request.Date(
    year=2020,
    month=1,
    day=1,
)
to_date = AccountOverview.Request.Date(
    year=today.year,
    month=today.month,
    day=today.day,
)
request = AccountOverview.Request(
    from_date=from_date,
    to_date=to_date,
)

# FETCH DATA
account_overview = trading_api.get_account_overview(
    request=request,
    raw=False,
)

# DISPLAY CASH MOVEMENTS
for cash_movement in account_overview.values['cashMovements']:
    print('date:', cash_movement['date'])
    print('valueDate:', cash_movement['valueDate'])
    print('productId:', dict(cash_movement).get('productId', 'unknown'))
    print('currency:', dict(cash_movement).get('currency', 'unknown'))
    print('change:', dict(cash_movement).get('change', 'unknown'))
