# IMPORTATIONS
import json
import logging

from quotecast.api import API as QuotecastAPI
from quotecast.pb.quotecast_pb2 import Quotecast

# SETUP LOGGING
logging.basicConfig(level=logging.INFO)

# SETUP CONFIG DICT
with open('config/config.json') as config_file:
    config_dict = json.load(config_file)

# SETUP CREDENTIALS
user_token = config_dict['user_token']  # HERE GOES YOUR USER_TOKEN

# SETUP API
quotecast_api = QuotecastAPI(user_token=user_token)

# BUILD REQUEST
request = Quotecast.Request()
request.subscriptions['AAPL.BATS,E'].extend([
    'LastDate',
    'LastTime',
    'LastPrice',
    'LastVolume',
    'LastPrice',
    'AskPrice',
    'BidPrice',
])

# FETCH METRICS
ticker_dict = quotecast_api.fetch_metrics(
    request=request,
)

print(ticker_dict)
