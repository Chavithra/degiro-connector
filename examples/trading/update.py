import json
import quotecast.helpers.pb_handler as pb_handler
import pandas as pd

from IPython.display import display
from trading.api import API as TradingAPI
from trading.pb.trading_pb2 import (
    Credentials,
    Update,
)
with open('config/config.json') as config_file:
    config = json.load(config_file)

int_account = config['int_account']
username = config['username']
password = config['password']
credentials = Credentials(
    int_account=int_account,
    username=username,
    password=password
)
trading_api = TradingAPI(credentials=credentials)

# INITIALIZATION

trading_api.connection_storage.connect()

print(trading_api.connection_storage.session_id)


request_list = Update.RequestList()
request_list.values.extend(
    [
        Update.Request(
            option=Update.Option.ORDERS,
            last_updated=0,
        ),
        Update.Request(
            option=Update.Option.PORTFOLIO,
            last_updated=0,
        ),
        Update.Request(
            option=Update.Option.TOTALPORTFOLIO,
            last_updated=0,
        ),
    ]
)

update = trading_api.get_update(request_list=request_list)
update_dict = pb_handler.build_dict_from_message(message=update)

if 'orders' in update_dict:
    orders_df = pd.DataFrame(update_dict['orders']['values'])
    print('orders')
    display(orders_df)

if 'portfolio' in update_dict:
    portfolio_df = pd.DataFrame(update_dict['portfolio']['values'])
    print('portfolio')
    display(portfolio_df)

if 'total_portfolio' in update_dict:
    total_portfolio_df = pd.DataFrame(update_dict['total_portfolio']['values'])
    print('total_portfolio')
    display(total_portfolio_df)