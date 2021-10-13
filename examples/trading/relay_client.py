# IMPORTATION STANDARD
import json
import logging

# IMPORTATION THIRD PARTY
import grpc
from google.protobuf.empty_pb2 import Empty

# from google.protobuf.wrappers_pb2 import *

# IMPORTATION INTERNAL
from degiro_connector.trading.models.trading_pb2 import Credentials
from degiro_connector.trading.models.trading_relay_pb2 import Config
from degiro_connector.trading.models.trading_relay_pb2_grpc import (
    TradingRelayStub,
)

# SETUP LOGS
logging.basicConfig(level=logging.DEBUG)

# SETUP CONFIG DICT
with open("config/config.json") as config_file:
    config_dict = json.load(config_file)

# SETUP CREDENTIALS
int_account = config_dict.get("int_account")
username = config_dict.get("username")
password = config_dict.get("password")
totp_secret_key = config_dict.get("totp_secret_key")
one_time_password = config_dict.get("one_time_password")

credentials = Credentials(
    int_account=int_account,
    username=username,
    password=password,
    totp_secret_key=totp_secret_key,
    one_time_password=one_time_password,
)

# SETUP RELAY
relay_channel = grpc.insecure_channel("localhost:50051")

relay_stub = TradingRelayStub(channel=relay_channel)

# RESPONSES DICT
responses = dict()

# CALL : set_config
with open("config/config.json") as config_file:
    config = json.load(config_file)
user_token = config["user_token"]

config = Config(credentials=credentials)
config.credentials.CopyFrom(credentials)
config.auto_connect = True

responses["set_config"] = relay_stub.set_config(request=config)

# CALL : connect
responses["connect"] = relay_stub.connect(request=Empty())

# CALL : get_config
responses["get_config"] = relay_stub.get_config(request=Empty())

# DISPLAY RESPONSES DICT
print(responses)
