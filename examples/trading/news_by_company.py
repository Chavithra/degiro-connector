import logging

from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.models.credentials import build_credentials
from degiro_connector.trading.models.news import NewsRequest

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

# SETUP REQUEST
news_request = NewsRequest(
    isin="NL0000235190",
    limit=10,
    offset=0,
    languages="en,fr",
)

# FETCH DATA
company_news = trading_api.get_news_by_company(news_request=news_request, raw=False)

print("Here are the company news :", company_news)
