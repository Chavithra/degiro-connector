# IMPORTATIONS STANDARD
import logging

# IMPORTATION THIRD PARTY
import pytest
import urllib3

# IMPORTATION INTERNAL
from degiro_connector.quotecast.api import API as QuotecastAPI

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
