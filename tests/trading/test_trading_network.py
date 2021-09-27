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
@pytest.mark.trading
@pytest.fixture(scope="module")
def trading(credentials) -> TradingAPI:
    return TradingAPI(credentials=credentials)


@pytest.mark.network
@pytest.mark.trading
def trading_connected(trading_connected) -> TradingAPI:
    trading_connected.connect()

    return trading_connected


# TESTS FIXTURES
@pytest.mark.network
@pytest.mark.trading
def test_fixture_trading_connected(trading_connected):
    session_id = trading_connected.connection_storage.session_id

    assert isinstance(session_id, str)
    assert len(session_id) == 45


# TESTS FEATURES
@pytest.mark.network
@pytest.mark.trading
def test_config_table(user_token, trading_api):
    time.sleep(random.uniform(0, 2))

    real_user_token = user_token
    real_session_id = trading_api.connection_storage.session_id
    config_table = trading_api.get_config()
    user_token = config_table["clientId"]
    session_id = config_table["sessionId"]

    assert user_token == real_user_token
    assert session_id == real_session_id


@pytest.mark.network
@pytest.mark.trading
def test_config_table_urls(trading_api):
    time.sleep(random.uniform(0, 2))

    config_table = trading_api.get_config()

    assert config_table["paUrl"] == "https://trader.degiro.nl/pa/secure/"
    assert (
        config_table["productSearchUrl"]
        == "https://trader.degiro.nl/product_search/secure/"
    )
    assert (
        config_table["companiesServiceUrl"]
        == "https://trader.degiro.nl/dgtbxdsservice/"
    )
    assert config_table["reportingUrl"] == "https://trader.degiro.nl/reporting/secure/"
    assert config_table["tradingUrl"] == "https://trader.degiro.nl/trading/secure/"
