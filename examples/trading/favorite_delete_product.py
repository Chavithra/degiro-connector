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
product_id = 1234567
list_id = 1234567
success = trading_api.delete_favorite_product(list_id=list_id, product_id=product_id)

if success:
    print(f"The following product was deleted : {product_id} => {list_id}")
else:
    print(f"Can't delete the following product : {product_id} => {list_id}")
