import logging
from time import sleep

from degiro_connector.core.exceptions import DeGiroConnectionError
from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.models.credentials import build_credentials

logging.basicConfig(level=logging.DEBUG)

def _wait_for_in_app_confirmation(trading_api: TradingAPI, in_app_token: str) -> bool:
    """Waits for the user to confirm in-app and retries connection until successful or unrecoverable error.
    Returns True if confirmation succeeds, otherwise raises exception."""
    trading_api.credentials.in_app_token = in_app_token
    while True:
        sleep(5)
        try:
            trading_api.connect()
            return True
        except DeGiroConnectionError as retry_error:
            if retry_error.error_details.status == 3:
                continue
            else:
                raise retry_error
        except Exception as e:
            raise e

credentials = build_credentials(
    location="config/config.json",
    # override={
    #     "username": "TEXT_PLACEHOLDER",
    #     "password": "TEXT_PLACEHOLDER",
    #     "int_account": NUMBER_PLACEHOLDER,  # From `get_client_details`
    #     # "totp_secret_key": "TEXT_PLACEHOLDER",  # For 2FA
    # },
)
session_id = None
trading_api = TradingAPI(credentials=credentials)
try:
    trading_api.connect()
    # ACCESS SESSION_ID
    session_id = trading_api.connection_storage.session_id
except DeGiroConnectionError as degiro_error:
    if degiro_error.error_details.status == 12:
        try:
            if _wait_for_in_app_confirmation(trading_api, degiro_error.error_details.in_app_token):
                # ACCESS SESSION_ID
                session_id = trading_api.connection_storage.session_id
        except Exception as e:
            print(f"Error during in-app confirmation: {e}")
    else:
        print(f"Error loging to Degiro: {degiro_error}")
        if degiro_error.error_details:
            print(degiro_error.error_details)
except ConnectionError as connection_error:
    print(f"ConnectionError: {connection_error}")

if session_id is not None:
    print("You are now connected, with the session id :", session_id)

# Don't see the notification? Use SMS verification
# https://trader.degiro.nl/login/secure/login/sms-new
# {
#     "captchaRequired": false,
#     "cellPhoneNumber": "*****867",
#     "smsCount": 1,
#     "status": 7,
#     "statusText": "smsNeeded"
# }
# Generated code is valid for only 30 seconds