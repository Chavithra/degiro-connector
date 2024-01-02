import json
import logging
from datetime import datetime, timedelta

from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.models.credentials import Credentials
from degiro_connector.trading.models.agenda import AgendaRequest, CalendarType

logging.basicConfig(level=logging.DEBUG)

with open("config/config.json") as config_file:
    config_dict = json.load(config_file)

credentials = Credentials.model_validate(obj=config_dict)
trading_api = TradingAPI(credentials=credentials)
trading_api.connect()

# FETCH AGENDA
agenda = trading_api.get_agenda(
    agenda_request=AgendaRequest(
        calendar_type=CalendarType.EARNINGS_CALENDAR,
        end_date=datetime.now(),
        start_date=datetime.now() - timedelta(days=1),
        offset=0,
        limit=25,
    ),
    raw=True,
)

print(agenda)
