import logging
import random
import time

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

# ACCESS SESSION_ID
session_id = trading_api.connection_storage.session_id

# Waiting
sleep_time = random.uniform(1, 5)
print(f"Waiting : {sleep_time}s ")
time.sleep(sleep_time)

# FETCH CONFIG TABLE
print(len(trading_api.get_config()))

# LOGOUT
print("Logout, session id : ", session_id)
trading_api.logout()

try:
    # FETCH CONFIG TABLE
    print(len(trading_api.get_config()))
except ConnectionError as e:
    print(e)
    print("Logout : success !")
else:
    print("Logout : fail !")
