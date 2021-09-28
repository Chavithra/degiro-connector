# IMPORTATIONS STANDARD
import logging

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
@pytest.fixture(scope="module")
def trading_connected(trading) -> TradingAPI:
    trading.connect()

    return trading
