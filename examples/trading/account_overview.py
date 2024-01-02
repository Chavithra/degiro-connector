import json
import logging
from datetime import date

from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.models.credentials import Credentials
from degiro_connector.trading.models.account import OverviewRequest

logging.basicConfig(level=logging.DEBUG)

with open("config/config.json") as config_file:
    config_dict = json.load(config_file)

credentials = Credentials.model_validate(obj=config_dict)
trading_api = TradingAPI(credentials=credentials)
trading_api.connect()

# FETCH ACCOUNT OVERVIEW
overview_request = OverviewRequest(
    from_date=date(year=date.today().year-1, month=1, day=1),
    to_date=date.today(),
)

account_overview = trading_api.get_account_overview(
    overview_request=overview_request,
    raw=False,
)

print(account_overview)
