import json
import logging
from datetime import date

from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.models.credentials import Credentials
from degiro_connector.trading.models.account import Format, ReportRequest

logging.basicConfig(level=logging.DEBUG)

with open("config/config.json") as config_file:
    config_dict = json.load(config_file)

credentials = Credentials.model_validate(obj=config_dict)
trading_api = TradingAPI(credentials=credentials)
trading_api.connect()

# FETCH REPORT
report = trading_api.get_position_report(
    report_request=ReportRequest(
        country="FR",
        lang="fr",
        format=Format.XLS,
        from_date=date(year=date.today().year - 1, month=1, day=1),
        to_date=date.today(),
    ),
    raw=False,
)

print(report)
