import logging

from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.models.credentials import build_credentials

logging.basicConfig(level=logging.DEBUG)

credentials = build_credentials(
    # location="config/config.json",
    override={
        "username": "PLACEHOLDER",
        "password": "PLACEHOLDER",
        "int_account": "PLACEHOLDER",  # Provided by `get_client_details`
        # "totp_secret_key": "PLACEHOLDER",  # For 2FA
    },
)
trading_api = TradingAPI(credentials=credentials)
trading_api.connect()

# ACCESS SESSION_ID
session_id = trading_api.connection_storage.session_id

print("You are now connected, with the session id :", session_id)
