# IMPORTATIONS STANDARD
import logging

# IMPORTATION THIRD PARTY
import pytest
import urllib3

# IMPORTATION INTERNAL

# SETUP LOGGING LEVEL
logging.basicConfig(level=logging.FATAL)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# TESTS FEATURES
@pytest.mark.trading
def test_logout(mocker, trading):
    # MOCK
    mocker.patch(
        "degiro_connector.trading.actions.action_logout.ActionLogout.connection_storage",
        mocker.Mock(session_id="MOCKING-SESSION"),
    )

    mock_response_raw = mocker.Mock()
    mock_response_raw.status_code = 200
    mocker.patch(
        "degiro_connector.trading.actions.action_logout.requests.Session.send",
        return_value=mock_response_raw,
    )

    # FETCH DATA
    response = trading.logout()

    # CHECK DATA
    assert response is True
