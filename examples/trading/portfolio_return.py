import logging

from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.models.credentials import build_credentials
from degiro_connector.trading.models.portfolio import (
    Period,
    PortfolioReturnRequest,
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

# FETCH PORTFOLIO RETURN
portfolio_return_request = PortfolioReturnRequest(
    period=Period.YTD,
)

portfolio_return = trading_api.get_portfolio_return(
    portfolio_return_request=portfolio_return_request,
    raw=False,
)

print(portfolio_return)
