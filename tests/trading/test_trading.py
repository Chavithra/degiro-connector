# IMPORTATIONS STANDARD
import logging
import random
import time

# IMPORTATION THIRD PARTY
import pytest
import urllib3

# IMPORTATION INTERNAL
from degiro_connector.trading.api import API as TradingAPI

# SETUP LOGGING LEVEL
logging.basicConfig(level=logging.FATAL)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# SETUP FIXTURES


@pytest.fixture(scope='module')
def trading_api(credentials) -> TradingAPI:
    trading_api = TradingAPI(credentials=credentials)
    trading_api.connect()

    return trading_api


# TESTS FIXTURES
def test_fixture_config_dict(credentials):

    assert isinstance(credentials.int_account, int)
    assert credentials.int_account > 0
    assert isinstance(credentials.username, str)
    assert len(credentials.username) > 0
    assert isinstance(credentials.password, str)
    assert len(credentials.password) > 0


def test_fixture_trading_api(trading_api):
    session_id = trading_api.connection_storage.session_id

    assert isinstance(session_id, str)
    assert len(session_id) == 45


# TESTS FEATURES
def test_config_table(user_token, trading_api):
    time.sleep(random.uniform(0, 2))

    real_user_token = user_token
    real_session_id = trading_api.connection_storage.session_id
    config_table = trading_api.get_config()
    user_token = config_table['clientId']
    session_id = config_table['sessionId']

    assert user_token == real_user_token
    assert session_id == real_session_id


def test_config_table_urls(trading_api):
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
