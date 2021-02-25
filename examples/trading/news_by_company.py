# IMPORTATIONS
import json
import logging

from trading.api import API as TradingAPI
from trading.pb.trading_pb2 import Credentials, NewsByCompany

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
request = NewsByCompany.Request(
    isin='NL0000235190',
    limit=10,
    offset=0,
    languages='en,fr',
)

# FETCH DATA
news_by_company = trading_api.get_news_by_company(request=request, raw=True)

# DISPLAY DATA
config_pretty = json.dumps(news_by_company, sort_keys=True, indent=4)

print('Here are the company news :', config_pretty)
