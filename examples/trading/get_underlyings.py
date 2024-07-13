import logging

from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.models.credentials import build_credentials
from degiro_connector.trading.models.product_search import UnderlyingsRequest

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

# FETCH UNDERLYINGS
underlying_list = trading_api.get_underlyings(
    underlyings_request=UnderlyingsRequest(
        future_exchange_id=1,
        # option_exchange_id=3,
    ),
    raw=False,
)

print(underlying_list)
