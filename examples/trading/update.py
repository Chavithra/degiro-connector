# IMPORTATIONS
import json
import logging
import quotecast.helpers.pb_handler as pb_handler
import pandas as pd

from IPython.display import display
from trading.api import API as TradingAPI
from trading.pb.trading_pb2 import Credentials, Update

# SETUP LOGGING LEVEL
logging.basicConfig(level=logging.DEBUG)

# SETUP CONFIG DICT
with open('config/config.json') as config_file:
    config = json.load(config_file)

# SETUP CREDENTIALS
int_account = config['int_account']
username = config['username']
password = config['password']
credentials = Credentials(
    int_account=int_account,
    username=username,
    password=password
)

# SETUP TRADING API
trading_api = TradingAPI(credentials=credentials)

# CONNECT
trading_api.connect()

# SETUP REQUEST
request_list = Update.RequestList()
request_list.values.extend([
    Update.Request(option=Update.Option.ORDERS, last_updated=0),
    Update.Request(option=Update.Option.PORTFOLIO, last_updated=0),
    Update.Request(option=Update.Option.TOTALPORTFOLIO, last_updated=0),
])

update = trading_api.get_update(request_list=request_list, raw=False)
update_dict = pb_handler.message_to_dict(message=update)

if 'orders' in update_dict:
    orders_df = pd.DataFrame(update_dict['orders']['values'])
    print('orders')
    display(orders_df)

if 'portfolio' in update_dict:
    portfolio_df = pd.DataFrame(update_dict['portfolio']['values'])
    print('portfolio')
    display(portfolio_df)

if 'total_portfolio' in update_dict:
    total_portfolio_df = pd.DataFrame(
        update_dict['total_portfolio']['values']
    )
    print('total_portfolio')
    display(total_portfolio_df)
