# IMPORTATIONS
import logging
import quotecast.helpers.pb_handler as pb_handler

from quotecast.api import API
from quotecast.models.quotecast_parser import QuotecastParser
from quotecast.pb.quotecast_pb2 import Request

# SETUP LOGGING LEVEL
logging.basicConfig(level=logging.INFO)

# SETUP API
api = API(user_token=12345) # to replace with your own "user_token"

# CONNECTION
api.connection_storage.connect()

# SUBSCRIBE TO FEED
request = Request(
    action=Request.Action.SUBSCRIBE,
    vwd_id='360015751',
    label_list=[
        'LastDate',
        'LastTime',
        'LastPrice',
        'LastVolume',
    ],
)
api.subscribe(request=request)

# SETUP JSON PARSER
quotecast_parser = QuotecastParser(fill_na=True)

while True:
    try:
        # FETCH DATA
        quotecast = api.fetch_data()

        # DISPLAY RAW JSON
        print(quotecast.json_data)

        # DISPLAY TICKER (PROTOBUF/GRPC OBJECT)
        quotecast_parser.put_quotecast(quotecast=quotecast)
        ticker = quotecast_parser.ticker
        print(ticker)

        # DISPLAY DICT
        record_list = pb_handler.build_dict_from_ticker(ticker=ticker)
        print(record_list)

        # DISPLAY PANDAS.DATAFRAME
        df = pb_handler.build_df_from_ticker(ticker=ticker)
        print(df)

        # REMOVE THIS LINE TO RUN IT IN LOOP
        # USE : CTRL+C TO QUIT
        break 

    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
