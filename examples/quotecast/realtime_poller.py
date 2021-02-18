# IMPORTATIONS
import json
import logging

from quotecast.api import API as QuotecastAPI
from quotecast.models.quotecast_parser import QuotecastParser
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

# CONNECTION
quotecast_api.connect()

# SUBSCRIBE TO METRICS
request = Quotecast.Request()
request.subscriptions['AAPL.BATS,E'].extend([
    'LastDate',
    'LastTime',
    'LastPrice',
    'LastVolume',
    'AskPrice',
    'BidPrice',
])
quotecast_api.subscribe(request=request)

# SETUP JSON PARSER
quotecast_parser = QuotecastParser()

while True:
    try:
        # FETCH DATA
        quotecast = quotecast_api.fetch_data()

        # DISPLAY RAW JSON
        print(quotecast.json_data)

        # DISPLAY TICKER (PROTOBUF/GRPC OBJECT)
        quotecast_parser.put_quotecast(quotecast=quotecast)
        ticker = quotecast_parser.ticker
        print(ticker)

        # DISPLAY DICT
        ticker_dict = quotecast_parser.ticker_dict
        print(ticker_dict)

        # DISPLAY PANDAS.DATAFRAME
        ticker_df = quotecast_parser.ticker_df
        print(ticker_df)

        # REMOVE THIS LINE TO RUN IT IN LOOP
        # USE : CTRL+C TO QUIT
        break

    except Exception as e:
        print(e)
        break
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
        break
