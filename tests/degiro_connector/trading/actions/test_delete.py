# IMPORTATIONS STANDARD
import datetime
import logging
import random
import time

import pytest
import urllib3

from degiro_connector.trading.models.trading_pb2 import (
    Order,
)

logging.basicConfig(level=logging.FATAL)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# TESTS FEATURES
@pytest.mark.trading
def test_delete_order(mocker, trading):
    # MOCK
    mock_order_id = "MOCKING-ORDER-ID"
    mocker.patch(
        "degiro_connector.trading.actions.action_delete_order.ActionDeleteOrder.connection_storage",
        mocker.Mock(session_id="MOCKING-SESSION"),
    )

    mock_response_raw = mocker.Mock()
    mock_response_raw.status_code = 200
    mocker.patch(
        "degiro_connector.trading.actions.action_delete_order.requests.Session.send",
        return_value=mock_response_raw,
    )

    # FETCH DATA
    response = trading.delete_order(order_id=mock_order_id)

    # CHECK DATA
    assert response is True
