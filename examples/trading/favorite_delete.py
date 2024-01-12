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

# DELETE AN EXISTING FAVORITE LIST
list_id = 1234567
success = trading_api.delete_favorite(list_id=list_id)

if success:
    print(f"The following list was deleted : {list_id}.")
else:
    print(f"Can't delete this list : {list_id}.")
