# IMPORTATIONS
import json
import logging

from degiro_connector.quotecast.api import API as QuotecastAPI
from degiro_connector.quotecast.pb.quotecast_pb2 import Chart

# SETUP LOGGING
logging.basicConfig(level=logging.INFO)

# SETUP CONFIG DICT
with open("config/config.json") as config_file:
    config_dict = json.load(config_file)

# SETUP CREDENTIALS
user_token = config_dict["user_token"]  # HERE GOES YOUR USER_TOKEN

# SETUP API
quotecast_api = QuotecastAPI(user_token=user_token)

# SUBSCRIBE TO METRICS
request = Chart.Request()
request.requestid = "1"
request.resolution = Chart.Interval.PT1M
request.culture = "fr-FR"
request.series.append("issueid:360148977")
request.series.append("price:issueid:360148977")
request.series.append("ohlc:issueid:360148977")
request.series.append("volume:issueid:360148977")
request.period = Chart.Interval.P1D
request.tz = "Europe/Paris"

# FETCH DATA
chart = quotecast_api.get_chart(
    request=request,
    override={"resolution":"P1D"},
    raw=True,
)

print(chart)
