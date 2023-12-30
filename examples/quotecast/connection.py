import json
import logging

from degiro_connector.quotecast.tools.ticker_fetcher import TickerFetcher

logging.basicConfig(level=logging.INFO)

with open("config/config.json") as config_file:
    config_dict = json.load(config_file)

user_token = config_dict.get("user_token")  # HERE GOES YOUR USER_TOKEN

session_id = TickerFetcher.get_session_id(user_token=user_token)

print("You are now connected, with the session id :", session_id)
