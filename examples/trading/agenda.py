import logging
from datetime import datetime, timedelta

from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.models.credentials import build_credentials
from degiro_connector.trading.models.agenda import AgendaRequest, CalendarType

logging.basicConfig(level=logging.DEBUG)

credentials = build_credentials(
    location="config/config.json",
    # override={
    #     "username": "TEXT_PLACEHOLDER",
    #     "password": "TEXT_PLACEHOLDER",
    #     "int_account": NUMBER_PLACEHOLDER,  # From `get_client_details`
    #     # "totp_secret_key": "TEXT_PLACEHOLDER",  # For 2FA
    # },
)
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
