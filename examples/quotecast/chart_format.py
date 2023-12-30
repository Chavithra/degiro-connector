# IMPORTATIONS
import json
import logging

from degiro_connector.quotecast.tools.chart_fetcher import ChartFetcher, ChartHelper
from degiro_connector.quotecast.models.chart import ChartRequest, Interval

# SETUP LOGGING
logging.basicConfig(level=logging.INFO)

# SETUP CONFIG DICT
with open("config/config.json") as config_file:
    config_dict = json.load(config_file)

# SETUP CREDENTIALS
user_token = config_dict.get("user_token")  # HERE GOES YOUR USER_TOKEN

# SETUP API
chart_fetcher = ChartFetcher(user_token=user_token)

# PREPARE REQUEST
chart_request = ChartRequest(
    culture = "fr-FR",
    # override={
    #     "resolution": "P1D",
    #     "period": "P1W",
    # },
    period = Interval.P1W,
    requestid = "1",
    resolution = Interval.P1D,
    series=[
        # "issueid:360148977",
        # "price:issueid:360148977",
        # "ohlc:issueid:360148977",
        # "volume:issueid:360148977",
        # "vwdkey:AAPL.BATS,E",
        # "price:vwdkey:AAPL.BATS,E",
        # "ohlc:vwdkey:AAPL.BATS,E",
        # "volume:vwdkey:AAPL.BATS,E",
    ],
    tz = "Europe/Paris",
)

# FETCH DATA
chart = chart_fetcher.get_chart(
    chart_request=chart_request,
    raw=False,
)

if chart:
    # By default a serie uses the order as `index`.
    # To have usable data, the `index` is formatted into `timestamp in seconds`.
    ChartHelper.format_chart(chart=chart, copy=False)

    # A `DataFrame` is easier to play with
    # Only series with the following types can be converted into a DataFrame :
    # - serie.type == "time"
    # - serie.type == "ohlc"
    # Beware of series with the following type :
    #  - serie.type == "object"
    # These are not actual timeseries and can't be converted into a DataFrame.
    chart0_df = ChartHelper.serie_to_df(serie=chart.series[0])

    # Having `datetime` as `index` is even more convenient
    # chart0_df["timestamp"] = pd.to_datetime(chart0_df["timestamp"], unit="s")

    # DISPLAY
    print(chart0_df)
