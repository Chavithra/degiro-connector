# IMPORTATIONS
import json
import logging

from degiro_connector.quotecast.api import API as QuotecastAPI
from degiro_connector.quotecast.models.quotecast_pb2 import Quotecast

# SETUP LOGGING
logging.basicConfig(level=logging.INFO)

# SETUP CONFIG DICT
with open("config/config.json") as config_file:
    config_dict = json.load(config_file)

# SETUP CREDENTIALS
user_token = config_dict.get("user_token")  # HERE GOES YOUR USER_TOKEN

# SETUP API
quotecast_api = QuotecastAPI(user_token=user_token)

# CONNECTION
quotecast_api.connect()

# BUILD REQUEST
request = Quotecast.Request()
request.subscriptions["AAPL.BATS,E"].extend(
    [
        "LastDate",
        "LastTime",
        "LastPrice",
        "LastVolume",
        "LastPrice",
        "AskPrice",
        "BidPrice",
    ]
)

# FETCH METRICS
ticker_dict = quotecast_api.fetch_metrics(
    request=request,
)

print(ticker_dict)
