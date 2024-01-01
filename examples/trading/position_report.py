import datetime
import json
import logging

from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.models.trading_pb2 import (
    PositionReport,
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
to_date = PositionReport.Request.Date(
    year=today.year,
    month=today.month,
    day=today.day,
)
request = PositionReport.Request(
    format=PositionReport.Format.CSV,
    country="FR",
    lang="fr",
    to_date=to_date,
)

# FETCH DATA
position_report = trading_api.get_position_report(
    request=request,
    raw=False,
)
format = position_report.Format.Name(position_report.format)
content = position_report.content

# DISPLAY FILE CONTENT
print("Format :", format)
print("Content :", content)
