import json
import logging

from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.models.credentials import build_credentials

logging.basicConfig(level=logging.DEBUG)

credentials = build_credentials(
    location="config/config.json",
    # override={
    #     "username": "TEXT_PLACEHOLDER",
    #     "password": "TEXT_PLACEHOLDER",
    #     # "totp_secret_key": "TEXT_PLACEHOLDER",  # For 2FA
    # },
)
trading_api = TradingAPI(credentials=credentials)
trading_api.connect()

# FETCH CONFIG TABLE
client_details_table = trading_api.get_client_details()

# EXTRACT DATA
int_account = client_details_table["data"]["intAccount"]
user_token = client_details_table["data"]["id"]
client_details_pretty = json.dumps(
    client_details_table,
    sort_keys=True,
    indent=4,
)

# DISPLAY DATA
print('Your "int_account" is :', int_account)
print('Your "user_token" is :', user_token)
print("Here is the rest your details :", client_details_pretty)
