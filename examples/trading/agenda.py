# IMPORTATIONS
import datetime
import json
import logging

from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.pb.trading_pb2 import (
    Agenda,
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
request = Agenda.Request()
request.start_date.FromJsonString('2021-06-21T22:00:00Z')
request.end_date.FromJsonString('2021-11-28T23:00:00Z')
request.calendar_type = Agenda.CalendarType.DIVIDEND_CALENDAR

# FETCH DATA
agenda = trading_api.get_agenda(
    request=request,
    raw=False,
)

# DISPLAY AGENDA
print('Agenda :', agenda)
