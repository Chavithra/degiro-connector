import json
import logging

import polars as pl

from degiro_connector.quotecast.tools.chart_fetcher import ChartFetcher, ChartFormatter
from degiro_connector.quotecast.models.chart import ChartRequest, Interval

logging.basicConfig(level=logging.INFO)

with open("config/config.json") as config_file:
    config_dict = json.load(config_file)

# FETCH CHART
user_token = config_dict.get("user_token")  # HERE GOES YOUR USER_TOKEN
chart_fetcher = ChartFetcher(user_token=user_token)
chart_request = ChartRequest(
    culture="fr-FR",
    # override={
    #     "resolution": "P1D",
    #     "period": "P1W",
    # },
    period=Interval.P1D,
    requestid="1",
    resolution=Interval.PT60M,
    series=[
        "issueid:360148977",
        "price:issueid:360148977",
        "ohlc:issueid:360148977",
        "volume:issueid:360148977",
        # "vwdkey:AAPL.BATS,E",
        # "price:vwdkey:AAPL.BATS,E",
        # "ohlc:vwdkey:AAPL.BATS,E",
        # "volume:vwdkey:AAPL.BATS,E",
    ],
    tz="Europe/Paris",
)

chart = chart_fetcher.get_chart(
    chart_request=chart_request,
    raw=False,
)

if chart:
    for series in chart.series:
        if ChartFormatter.can_format(series=series):
            df = ChartFormatter.format_series(series=series)
        else:
            df = pl.DataFrame(series.data)
        print(df)
