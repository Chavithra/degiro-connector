# IMPORTATIONS
import logging

from quotecast.api import API
from quotecast.pb.quotecast_pb2 import (
    Request,
)

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
    data = api.fetch_data()