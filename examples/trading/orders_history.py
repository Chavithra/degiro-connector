import logging
from datetime import date

from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.models.credentials import build_credentials
from degiro_connector.trading.models.order import HistoryRequest

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

# FETCH HISTORY
orders_history = trading_api.get_orders_history(
    history_request=HistoryRequest(
        from_date=date(year=date.today().year, month=1, day=1),
        to_date=date.today(),
    ),
    raw=False,
)

print(orders_history)
