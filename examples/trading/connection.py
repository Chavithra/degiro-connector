import logging

from degiro_connector.core.exceptions import DeGiroConnectionError
from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.models.credentials import build_credentials

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
try:
    trading_api.connect()
except DeGiroConnectionError as degiro_error:
    print(f"Error loging to Degiro: {degiro_error}")
    if degiro_error.error_details:
        print(degiro_error.error_details)
except ConnectionError as connection_error:
    print(f"ConnectionError: {connection_error}")
else:
    # ACCESS SESSION_ID
    session_id = trading_api.connection_storage.session_id

    print("You are now connected, with the session id :", session_id)
