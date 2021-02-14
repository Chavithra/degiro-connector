# IMPORTATIONS
import json

from quotecast.api import API as QuotecastAPI

# SETUP CONFIG DICT
with open('config/config.json') as config_file:
    config_dict = json.load(config_file)

# SETUP CREDENTIALS
user_token = config_dict['user_token']  # HERE GOES YOUR USER_TOKEN

# SETUP API
quotecast_api = QuotecastAPI(user_token=user_token)

# CONNECTION
quotecast_api.connect()

# ACCESS SESSION_ID
session_id = quotecast_api.connection_storage.session_id

print('You are now connected, with the session id :', session_id)
