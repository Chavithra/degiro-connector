import json
import logging

from degiro_connector.quotecast.models.ticker import TickerRequest
from degiro_connector.quotecast.tools.ticker_fetcher import TickerFetcher
from degiro_connector.quotecast.tools.ticker_to_df import TickerToDF

logging.basicConfig(level=logging.INFO)

with open("config/config.json") as config_file:
    config_dict = json.load(config_file)

user_token = config_dict.get("user_token")  # HERE GOES YOUR USER_TOKEN

logger = TickerFetcher.build_logger()
session = TickerFetcher.build_session()
ticker_to_df = TickerToDF()
ticker_request = TickerRequest(
    request_type="subscription",
    request_map={
        "360015751": [
            "LastDate",
            "LastTime",
            "LastPrice",
            "LastVolume",
        ],
        "AAPL.BATS,E": [
            "LastDate",
            "LastTime",
            "LastPrice",
            "LastVolume",
        ],
    },
)

session_id = TickerFetcher.get_session_id(user_token=user_token)

if session_id is None:
    raise TypeError("`session_id` is None")

TickerFetcher.subscribe(
    ticker_request=ticker_request,
    session_id=session_id,
    session=session,
    logger=logger,
)

ticker = TickerFetcher.fetch_ticker(
    session_id=session_id,
    session=session,
    logger=logger,
)

if ticker is None:
    raise TypeError("`ticker` is None")

df = ticker_to_df.parse(ticker=ticker)

print(df)
