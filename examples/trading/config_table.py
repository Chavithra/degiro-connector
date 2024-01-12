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
    #     "int_account": NUMBER_PLACEHOLDER,  # From `get_client_details`
    #     # "totp_secret_key": "TEXT_PLACEHOLDER",  # For 2FA
    # },
)
trading_api = TradingAPI(credentials=credentials)
trading_api.connect()

# FETCH CONFIG TABLE
config_table = trading_api.get_config()

# EXTRACT DATA
user_token = config_table["clientId"]
session_id = config_table["sessionId"]

# DISPLAY DATA
config_pretty = json.dumps(config_table, sort_keys=True, indent=4)

print('Your "user_token" is :', user_token)
print("Here is the rest of config :", config_pretty)
