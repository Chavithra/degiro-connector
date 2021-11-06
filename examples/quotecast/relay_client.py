# IMPORTATION STANDARD
import json
import logging

# IMPORTATION THIRD PARTY
import grpc
from google.protobuf.empty_pb2 import Empty

# from google.protobuf.wrappers_pb2 import *

# IMPORTATION INTERNAL
from degiro_connector.quotecast.models.quotecast_pb2 import Chart, Quotecast
from degiro_connector.quotecast.models.quotecast_relay_pb2 import SetConfig
from degiro_connector.quotecast.models.quotecast_relay_pb2_grpc import (
    QuotecastRelayStub,
)

# SETUP LOGS
logging.basicConfig(level=logging.DEBUG)

# SETUP CONFIG DICT
with open("config/config.json") as config_file:
    config_dict = json.load(config_file)

# SETUP CREDENTIALS
user_token = config_dict.get("user_token")

# SETUP RELAY
relay_channel = grpc.insecure_channel("localhost:50051")
relay_stub = QuotecastRelayStub(channel=relay_channel)

# RESPONSES DICT
responses = dict()

# CALL : set_config
set_config = SetConfig()
set_config.user_token = user_token
set_config.auto_connect = True

responses["set_config"] = relay_stub.set_config(request=set_config)

# CALL : connect
responses["connect"] = relay_stub.connect(request=Empty())

# CALL : subscribe
request = Quotecast.Request()
request.subscriptions["AAPL.BATS,E"].extend(
    [
        "LastDate",
        "LastTime",
        "LastPrice",
        "LastVolume",
        "AskPrice",
        "BidPrice",
    ]
)

responses["subscribe"] = relay_stub.subscribe(request=request)

# CALL : fetch_data
responses["fetch_data"] = relay_stub.fetch_data(request=Empty())


# CALL : get_chart
request = Chart.Request()
request.culture = "fr-FR"
request.period = Chart.Interval.PT1H
request.requestid = "1"
request.resolution = Chart.Interval.P1D
# request.series.append("issueid:360148977")
# request.series.append("price:issueid:360148977")
request.series.append("ohlc:issueid:360148977")
# request.series.append("volume:issueid:360148977")
# request.series.append("vwdkey:AAPL.BATS,E")
# request.series.append("price:vwdkey:AAPL.BATS,E")
# request.series.append("ohlc:vwdkey:AAPL.BATS,E")
# request.series.append("volume:vwdkey:AAPL.BATS,E")
request.tz = "Europe/Paris"
request.tz = "Europe/Paris"
request.override["resolution"] = "P1D"
request.override["period"] = "P1W"

responses["get_chart"] = relay_stub.get_chart(
    request=request,
)
# DISPLAY RESPONSES DICT
print(responses)
