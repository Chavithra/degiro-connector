import json
import logging

import polars as pl

from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.models.credentials import Credentials

logging.basicConfig(level=logging.DEBUG)

with open("config/config.json") as config_file:
    config_dict = json.load(config_file)

credentials = Credentials.model_validate(obj=config_dict)

trading_api = TradingAPI(credentials=credentials)

trading_api.connect()

# GET FAVORITES
favorite_batch = trading_api.get_favorite(raw=False)

favorite_df = pl.DataFrame(favorite_batch.data)

print(favorite_df)
