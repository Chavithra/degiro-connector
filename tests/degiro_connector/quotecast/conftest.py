# IMPORTATIONS STANDARD
import logging

# IMPORTATION THIRD PARTY
import pytest
import urllib3

# IMPORTATION INTERNAL
from degiro_connector.quotecast.api import API as QuotecastAPI
from degiro_connector.quotecast.models.quotecast_pb2 import Chart

# SETUP LOGGING
logging.basicConfig(level=logging.FATAL)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# SETUP FIXTURES
@pytest.mark.quotecast
@pytest.fixture(scope="module")
def quotecast(user_token) -> QuotecastAPI:
    return QuotecastAPI(user_token=user_token)


@pytest.mark.quotecast
@pytest.mark.network
@pytest.fixture(scope="module")
def quotecast_connected(quotecast) -> QuotecastAPI:
    quotecast.connect()

    return quotecast


@pytest.mark.quotecast
@pytest.fixture(scope="module")
def stock_request() -> Chart.Request:
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

    return request
