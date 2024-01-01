import datetime
import json
import logging

from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.models.trading_pb2 import (
    AccountOverview,
    Credentials,
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
from_date = AccountOverview.Request.Date(
    year=today.year,
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
for cash_movement in account_overview.values["cashMovements"]:
    print("date:", cash_movement["date"])
    print("valueDate:", cash_movement["valueDate"])
    print("productId:", dict(cash_movement).get("productId", "unknown"))
    print("currency:", dict(cash_movement).get("currency", "unknown"))
    print("change:", dict(cash_movement).get("change", "unknown"))
