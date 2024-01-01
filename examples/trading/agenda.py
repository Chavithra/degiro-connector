import json
import logging

from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.models.trading_pb2 import (
    Agenda,
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
request = Agenda.Request()
request.start_date.FromJsonString("2021-06-21T22:00:00Z")
request.end_date.FromJsonString("2021-11-28T23:00:00Z")
request.calendar_type = Agenda.CalendarType.DIVIDEND_CALENDAR
request.offset = 0
request.limit = 25  # 0 < limit <= 100

# FETCH DATA
agenda = trading_api.get_agenda(
    request=request,
    raw=False,
)

# DISPLAY AGENDA
print("Agenda :", agenda)
