import json
import logging

from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.models.credentials import Credentials
from degiro_connector.trading.models.trading_pb2 import Order

logging.basicConfig(level=logging.DEBUG)

with open("config/config.json") as config_file:
    config_dict = json.load(config_file)

credentials = Credentials.model_validate(obj=config_dict)

# SETUP TRADING API
trading_api = TradingAPI(credentials=credentials)

# ESTABLISH CONNECTION
trading_api.connect()

# SETUP ORDER
order = Order(
    action=Order.Action.BUY,
    order_type=Order.OrderType.LIMIT,
    price=10,
    product_id=71981,
    size=1,
    time_type=Order.TimeType.GOOD_TILL_DAY,
)

# FETCH CHECKING_RESPONSE
checking_response = trading_api.check_order(order=order)

# EXTRACT CONFIRMATION_ID
confirmation_id = checking_response.confirmation_id

# EXTRACT OTHER DATA
free_space_new = checking_response.free_space_new
response_datetime = checking_response.response_datetime
transaction_fees = checking_response.transaction_fees
transaction_opposite_fees = checking_response.transaction_opposite_fees
transaction_taxes = checking_response.transaction_taxes

# SEND CONFIRMATION
confirmation_response = trading_api.confirm_order(
    confirmation_id=confirmation_id, order=order
)

print(checking_response)
print(confirmation_response)
