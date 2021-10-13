# IMPORTATION STANDARD
import json

# IMPORTATION THIRD PARTY

# IMPORTATION INTERNAL
from degiro_connector.quotecast.relay import Relay as QuotecastRelay

# SETUP CONFIG DICT
with open("config/config.json") as config_file:
    config_dict = json.load(config_file)

# SETUP CREDENTIALS
user_token = config_dict.get("user_token")

relay = QuotecastRelay(user_token=0)
relay.serve()
