# IMPORTATIONS
import json
import logging
import pytest
import random
import time
import urllib3

from quotecast.api import API as QuotecastAPI
from quotecast.pb.quotecast_pb2 import Chart

# SETUP LOGGING
logging.basicConfig(level=logging.FATAL)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

@pytest.fixture(scope='module')
def config_dict():
    with open('config/config.json') as config_file:
        config_dict = json.load(config_file)

    return config_dict

@pytest.fixture(scope='module')
def user_token(config_dict):
    user_token = config_dict['user_token']

    return user_token

@pytest.fixture(scope='module')
def quotecast_api(user_token):
    quotecast_api = QuotecastAPI(user_token=user_token)
    quotecast_api.connect()

    return quotecast_api

def test_session_id(quotecast_api):
    time.sleep(random.uniform(0, 2))

    session_id = quotecast_api.connection_storage.session_id

    assert isinstance(session_id, str)
    assert len(session_id) == 36

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

    assert  b_series_0_data_keys == series_0_data_keys
    assert chart['requestid'] == '1'
    assert chart['resolution'] == 'PT1M'
    assert chart['series'][0]['data']['quality'] == 'REALTIME'
    assert chart['series'][0]['data']['issueId'] == 360148977