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

# TESTS FIXTURES
@pytest.mark.quotecast
def test_fixture_quotecast(quotecast):
    assert isinstance(quotecast, QuotecastAPI)


@pytest.mark.quotecast
@pytest.mark.network
def test_fixture_quotecast_connected(quotecast_connected):
    session_id = quotecast_connected.connection_storage.session_id

    assert isinstance(session_id, str)
    assert len(session_id) == 36
