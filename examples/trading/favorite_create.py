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

# CREATE A FAVORITE LIST
name = "SOME_LIST"
favorite_id = trading_api.create_favorite(name=name)

if favorite_id:
    print(f"The following list was created : {name} = {favorite_id}.")
else:
    print(f"Can't create this list : {name}.")
