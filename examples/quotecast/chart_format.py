# IMPORTATIONS
import json
import logging
import pandas as pd

from degiro_connector.quotecast.api import API as QuotecastAPI
from degiro_connector.quotecast.actions.action_get_chart import ChartHelper
from degiro_connector.quotecast.models.quotecast_pb2 import Chart

# SETUP LOGGING
logging.basicConfig(level=logging.INFO)

# SETUP CONFIG DICT
with open("config/config.json") as config_file:
    config_dict = json.load(config_file)

# SETUP CREDENTIALS
user_token = config_dict.get("user_token")  # HERE GOES YOUR USER_TOKEN

# SETUP API
quotecast_api = QuotecastAPI(user_token=user_token)

# PREPARE REQUEST
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

# FETCH DATA
chart = quotecast_api.get_chart(
    request=request,
    raw=False,
)

# By default a serie uses the order as `index`.
# To have usable data, the `index` is formatted into `timestamp in seconds`.
ChartHelper.format_chart(chart=chart, copy=False)

# A `DataFrame` is easier to play with
# Only series with the following types can be converted into DataFrame :
# - serie.type == "time"
# - serie.type == "ohlc"
# Beware of series with the following type :
#  - serie.type == "object"
# These are not actual timeseries and can't converted into DataFrame.
chart0_df = ChartHelper.serie_to_df(serie=chart.series[0])

# Having `datetime` as `index` is even more convenient
chart0_df["timestamp"] = pd.to_datetime(chart0_df["timestamp"], unit="s")

# DISPLAY
print(chart0_df)
