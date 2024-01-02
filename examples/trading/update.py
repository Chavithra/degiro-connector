import json
import logging

# from IPython.display import display
from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.models.credentials import Credentials
from degiro_connector.trading.models.account import UpdateOption, UpdateRequest

logging.basicConfig(level=logging.DEBUG)

with open("config/config.json") as config_file:
    config_dict = json.load(config_file)

credentials = Credentials.model_validate(obj=config_dict)
trading_api = TradingAPI(credentials=credentials)
trading_api.connect()

# FETCH ACCOUNT UPDATE
account_update = trading_api.get_update(
    request_list=[
        UpdateRequest(
            option=UpdateOption.ALERTS,
            last_updated=0,
        ),
        UpdateRequest(
            option=UpdateOption.CASH_FUNDS,
            last_updated=0,
        ),
        UpdateRequest(
            option=UpdateOption.HISTORICAL_ORDERS,
            last_updated=0,
        ),
        UpdateRequest(
            option=UpdateOption.ORDERS,
            last_updated=0,
        ),
        UpdateRequest(
            option=UpdateOption.PORTFOLIO,
            last_updated=0,
        ),
        UpdateRequest(
            option=UpdateOption.TOTAL_PORTFOLIO,
            last_updated=0,
        ),
        UpdateRequest(
            option=UpdateOption.TRANSACTIONS,
            last_updated=0,
        ),
    ],
    raw=True,
)

print(account_update)
