# IMPORTATIONS
import logging
import pandas as pd

from google.protobuf import json_format
from quotecast.api import API
from quotecast.models.quotecast_parser import (
    QuotecastParser,
)
from quotecast.pb.quotecast_pb2 import (
    Request,
)

# SETUP LOGGING LEVEL
logging.basicConfig(level=logging.INFO)

# SETUP QUOTECASTPARSER
quotecast_parser = QuotecastParser(fill_na=True)

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
        'OpenPrice',
        'HighPrice',
        'LowPrice',
        'ClosePrice',
        'PreviousClosePrice',
    ],
)
api.subscribe(request=request)

while True:
    # FETCH DATA
    quotecast = api.fetch_data()

    # BUILD TICKER
    quotecast_parser.put_quotecast(quotecast=quotecast)
    ticker = quotecast_parser.ticker
    
    # DISPLAY TICKER
    ticker_dict = json_format.MessageToDict(
        message=ticker,
        including_default_value_fields=True,
        preserving_proto_field_name=True,
    )
    ticker_df = pd.DataFrame(ticker_dict['metric_list'])
    print(ticker_df)
