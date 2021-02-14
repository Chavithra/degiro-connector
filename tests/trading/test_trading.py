# IMPORTATIONS
import json
import logging
import pytest
import random
import time
import urllib3

from trading.api import API as TradingAPI
from trading.pb.trading_pb2 import Credentials

# SETUP LOGGING LEVEL
logging.basicConfig(level=logging.FATAL)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# SETUP FIXTURES
@pytest.fixture(scope='module')
def config_dict():
    with open('config/config.json') as config_file:
        config_dict = json.load(config_file)

    return config_dict


@pytest.fixture(scope='module')
def credentials(config_dict):
    int_account = config_dict['int_account']
    username = config_dict['username']
    password = config_dict['password']

    credentials = Credentials(
        int_account=int_account,
        username=username,
        password=password,
    )

    return credentials


@pytest.fixture(scope='module')
def trading_api(credentials):
    trading_api = TradingAPI(credentials=credentials)
    trading_api.connect()

    return trading_api


# TESTS FIXTURES
def test_fixture_config_dict(config_dict):
    int_account = config_dict['int_account']
    username = config_dict['username']
    password = config_dict['password']

    assert isinstance(int_account, int)
    assert int_account > 0
    assert isinstance(username, str)
    assert len(username) > 0
    assert isinstance(password, str)
    assert len(password) > 0


def test_fixture_trading_api(trading_api):
    session_id = trading_api.connection_storage.session_id

    assert isinstance(session_id, str)
    assert len(session_id) == 45


# TESTS FEATURES
def test_config_table(config_dict, trading_api):
    time.sleep(random.uniform(0, 2))

    real_user_token = config_dict['user_token']
    real_session_id = trading_api.connection_storage.session_id
    config_table = trading_api.get_config()
    user_token = config_table['clientId']
    session_id = config_table['sessionId']

    assert user_token == real_user_token
    assert session_id == real_session_id


def test_config_table_urls(config_dict, trading_api):
    time.sleep(random.uniform(0, 2))

    config_table = trading_api.get_config()

    assert config_table['paUrl'] == \
        'https://trader.degiro.nl/pa/secure/'
    assert config_table['productSearchUrl'] == \
        'https://trader.degiro.nl/product_search/secure/'
    assert config_table['companiesServiceUrl'] == \
        'https://trader.degiro.nl/dgtbxdsservice/'
    assert config_table['reportingUrl'] == \
        'https://trader.degiro.nl/reporting/secure/'
    assert config_table['tradingUrl'] == \
        'https://trader.degiro.nl/trading/secure/'
