import json
import logging

import polars as pl
from pydantic import BaseModel

from degiro_connector.quotecast.tools.chart_fetcher import ChartFetcher
from degiro_connector.quotecast.models.chart import ChartRequest, Interval

logging.basicConfig(level=logging.INFO)

with open("config/config.json") as config_file:
    config_dict = json.load(config_file)
user_token = config_dict.get("user_token")  # HERE GOES YOUR USER_TOKEN

# FETCH CHART
chart_fetcher = ChartFetcher(user_token=user_token)
chart_request = ChartRequest(
    culture="fr-FR",
    # override={
    #     "resolution": "P1D",
    #     "period": "P1W",
    # },
    period=Interval.P1D,
    requestid="1",
    resolution=Interval.PT1H,
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

if isinstance(chart, BaseModel):
    for series in chart.series:
        print(pl.DataFrame(data=series.data, orient="row"))

if isinstance(chart, dict):
    print(chart)
