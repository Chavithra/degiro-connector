# IMPORTATIONS
import json
import logging

from trading.api import API as TradingAPI
from trading.pb.trading_pb2 import Credentials, LatestNews

# SETUP LOGGING LEVEL
logging.basicConfig(level=logging.DEBUG)

# SETUP CONFIG DICT
with open('config/config.json') as config_file:
    config_dict = json.load(config_file)

# SETUP CREDENTIALS
username = config_dict['username']
password = config_dict['password']

credentials = Credentials(
    int_account=None,
    username=username,
    password=password,
)

# SETUP TRADING API
trading_api = TradingAPI(credentials=credentials)

# CONNECT
trading_api.connect()

# SETUP REQUEST
request = LatestNews.Request(
    offset=0,
    languages='en,fr',
    limit=20,
)

# FETCH DATA
latest_news = trading_api.get_latest_news(request=request, raw=True)

# DISPLAY DATA
config_pretty = json.dumps(latest_news, sort_keys=True, indent=4)

print('Here are the latest news :', config_pretty)
