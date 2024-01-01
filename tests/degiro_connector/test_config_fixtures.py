# IMPORTATIONS STANDARD
import logging

import pytest
import urllib3


logging.basicConfig(level=logging.FATAL)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# TEST FIXTURES
@pytest.mark.quotecast
def test_fixture_user_token(user_token):
    assert isinstance(user_token, int)
    assert user_token > 0


@pytest.mark.trading
def test_fixture_credentials(credentials):
    assert isinstance(credentials.int_account, int)
    assert credentials.int_account > 0
    assert isinstance(credentials.username, str)
    assert len(credentials.username) > 0
    assert isinstance(credentials.password, str)
    assert len(credentials.password) > 0
