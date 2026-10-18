import logging

from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.models.credentials import build_credentials
from degiro_connector.trading.models.portfolio import (
    Period,
    PortfolioValueRequest,
)

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

# FETCH PORTFOLIO VALUE
portfolio_value_request = PortfolioValueRequest(
    period=Period.YTD,
)

portfolio_value = trading_api.get_portfolio_value(
    portfolio_value_request=portfolio_value_request,
    raw=False,
)

print(portfolio_value)
