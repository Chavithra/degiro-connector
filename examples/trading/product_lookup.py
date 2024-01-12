import logging

from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.models.credentials import build_credentials
from degiro_connector.trading.models.product_search import LookupRequest


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

# FETCH PRODUCTS
lookup_request = LookupRequest(
    search_text="APPLE",
    limit=2,
    offset=0,
    product_type_id=1,
)

product_batch = trading_api.product_search(product_request=lookup_request, raw=False)

print(product_batch)
