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

# UPDATE A FAVORITE LIST NAME
id = 1234567
name = "SOME_OTHER_NAME"
success = trading_api.rename_favorite(id=id, name=name)

# DISPLAY - MESSAGE
if success:
    print(f"The following list was update : {name} = {id}.")
else:
    print(f"Can't update this list : {name} =  = {id}.")
