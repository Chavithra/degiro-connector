# IMPORTATIONS
import logging
import quotecast.helpers.pb_handler as pb_handler

from quotecast.api import API as QuotecastAPI
from quotecast.models.quotecast_parser import QuotecastParser
from quotecast.pb.quotecast_pb2 import Quotecast

# SETUP LOGGING
logging.basicConfig(level=logging.INFO)

# SETUP CREDENTIALS
user_token = 0 # TO REPLACE WITH YOUR USER TOKEN

# SETUP API
quotecast_api = QuotecastAPI(user_token=user_token)

# CONNECTION
quotecast_api.connect()

# ACCESS SESSION_ID
session_id = quotecast_api.connection_storage.session_id

# SUBSCRIBE TO METRICS
request = Quotecast.Request()
request.subscriptions['AAPL.BATS,E'].extend([
    'LastDate',
    'LastTime',
    'LastPrice',
    'LastVolume',
])
quotecast_api.subscribe(request=request)

# SETUP JSON PARSER
quotecast_parser = QuotecastParser(forward_fill=True)

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
        record_list = pb_handler.ticker_to_dict(ticker=ticker)
        print(record_list)

        # DISPLAY PANDAS.DATAFRAME
        df = pb_handler.ticker_to_df(ticker=ticker)
        print(df)

        # REMOVE THIS LINE TO RUN IT IN LOOP
        # USE : CTRL+C TO QUIT
        break 

    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
