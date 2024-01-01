import json
import logging

from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.models.credentials import Credentials
from degiro_connector.trading.models.order import Action, Order, OrderType, TimeType

logging.basicConfig(level=logging.DEBUG)

with open("config/config.json") as config_file:
    config_dict = json.load(config_file)

credentials = Credentials.model_validate(obj=config_dict)
trading_api = TradingAPI(credentials=credentials)
trading_api.connect()

# PASS ORDER
order = Order(
    buy_sell=Action.BUY,
    order_type=OrderType.LIMIT,
    price=12.1,
    product_id=72160,
    size=1,
    time_type=TimeType.GOOD_TILL_DAY,
)

checking_response = trading_api.check_order(order=order)
print(checking_response)

confirmation_response = trading_api.confirm_order(
    confirmation_id=checking_response.confirmation_id,
    order=order,
)
print(confirmation_response)
