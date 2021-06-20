# IMPORTATIONS STANDARD
import logging
import random
import time

# IMPORTATION THIRD PARTY
import pytest
import urllib3

# IMPORTATION INTERNAL
import degiro_connector.quotecast.helpers.pb_handler as pb_handler
import degiro_connector.quotecast.utilities as utilities
from degiro_connector.quotecast.api import API as QuotecastAPI
from degiro_connector.quotecast.models.quotecast_parser import QuotecastParser
from degiro_connector.quotecast.pb.quotecast_pb2 import Chart, Quotecast

# SETUP LOGGING
logging.basicConfig(level=logging.FATAL)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# SETUP FIXTURES
@pytest.fixture(scope='module')
def quotecast_api(user_token) -> QuotecastAPI:
    quotecast_api = QuotecastAPI(user_token=user_token)
    quotecast_api.connect()

    return quotecast_api


# TESTS FIXTURES
def test_fixture_user_token(user_token):
    assert isinstance(user_token, int)
    assert user_token > 0


def test_fixture_quotecast_api(quotecast_api):
    session_id = quotecast_api.connection_storage.session_id

    assert isinstance(session_id, str)
    assert len(session_id) == 36


# TESTS FEATURES
def test_chart(quotecast_api):
    time.sleep(random.uniform(0, 2))

    request = Chart.Request()
    request.requestid = '1'
    request.resolution = Chart.Resolution.PT1M
    request.culture = 'fr-FR'
    request.series.append('issueid:360148977')
    request.series.append('price:issueid:360148977')
    request.series.append('ohlc:issueid:360148977')
    request.series.append('volume:issueid:360148977')
    request.period = Chart.Period.P1D
    request.tz = 'Europe/Paris'

    # FETCH DATA
    chart = quotecast_api.get_chart(
        request=request,
        override=None,
        raw=True,
    )

    b_series_0_data_keys = [
        'issueId',
        'companyId',
        'name',
        'identifier',
        'isin',
        'alfa',
        'market',
        'currency',
        'type',
        'quality',
        'lastPrice',
        'lastTime',
        'absDiff',
        'relDiff',
        'highPrice',
        'highTime',
        'lowPrice',
        'lowTime',
        'openPrice',
        'openTime',
        'closePrice',
        'closeTime',
        'cumulativeVolume',
        'previousClosePrice',
        'previousCloseTime',
        'tradingStartTime',
        'tradingEndTime',
        'tradingAddedTime',
        'lowPriceP1Y',
        'highPriceP1Y',
        'windowStart',
        'windowEnd',
        'windowFirst',
        'windowLast',
        'windowHighTime',
        'windowHighPrice',
        'windowLowTime',
        'windowLowPrice',
        'windowOpenTime',
        'windowOpenPrice',
        'windowPreviousCloseTime',
        'windowPreviousClosePrice',
        'windowTrend'
    ]

    series_0_data_keys = list(chart['series'][0]['data'].keys())

    assert b_series_0_data_keys == series_0_data_keys
    assert chart['requestid'] == '1'
    assert chart['resolution'] == 'PT1M'
    assert chart['series'][0]['data']['quality'] == 'REALTIME'
    assert chart['series'][0]['data']['issueId'] == 360148977


def test_quotecast(quotecast_api):
    time.sleep(random.uniform(0, 2))

    request = Quotecast.Request()
    request.subscriptions['AAPL.BATS,E'].extend([
        'LastDate',
        'LastTime',
        'LastPrice',
        'LastVolume',
        'AskPrice',
        'BidPrice',
    ])
    quotecast_api.subscribe(request=request)

    quotecast = quotecast_api.fetch_data()

    quotecast_parser = QuotecastParser()
    quotecast_parser.put_quotecast(quotecast=quotecast)
    ticker = quotecast_parser.ticker
    ticker_dict = pb_handler.message_to_dict(message=ticker)
    metrics = ticker_dict['products']['AAPL.BATS,E']['metrics']

    assert 'AAPL.BATS,E' in ticker.product_list

    for metric in metrics:
        assert isinstance(metrics[metric], float)


def test_build_logger():
    time.sleep(random.uniform(0, 2))

    logger = utilities.build_logger()
    
    assert isinstance(logger, logging.Logger)