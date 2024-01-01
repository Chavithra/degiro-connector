# IMPORTATIONS STANDARD
import logging

import pytest
import urllib3

from degiro_connector.trading.api import API as TradingAPI

logging.basicConfig(level=logging.FATAL)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# SETUP FIXTURES
@pytest.mark.trading
@pytest.fixture(scope="function")
def trading(credentials) -> TradingAPI:
    return TradingAPI(credentials=credentials)


@pytest.mark.network
@pytest.mark.trading
@pytest.fixture(scope="module")
def trading_connected(credentials) -> TradingAPI:
    trading = TradingAPI(credentials=credentials)
    trading.connect()

    return trading
