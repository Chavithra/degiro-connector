# IMPORTATIONS STANDARD
import logging

import pytest
import requests
import urllib3

from degiro_connector.quotecast.models.chart import Chart, ChartRequest, Interval
from degiro_connector.quotecast.tools.ticker_fetcher import TickerFetcher

# SETUP LOGGING
logging.basicConfig(level=logging.FATAL)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# SETUP FIXTURES
@pytest.mark.quotecast
@pytest.fixture(scope="module")
def logger() -> logging.Logger:
    return TickerFetcher.build_logger()

@pytest.mark.quotecast
@pytest.fixture(scope="module")
def session() -> requests.Session:
    return TickerFetcher.build_session()


@pytest.mark.quotecast
@pytest.fixture(scope="module")
def stock_request() -> ChartRequest:
    chart_request = ChartRequest(
        culture = "fr-FR",
        # override={
        #     "resolution": "P1D",
        #     "period": "P1W",
        # },
        period = Interval.P1D,
        requestid = "1",
        resolution = Interval.PT1H,
        series=[
            "issueid:360148977",
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

    return chart_request
