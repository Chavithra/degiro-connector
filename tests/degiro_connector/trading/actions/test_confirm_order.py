# IMPORTATIONS STANDARD
import datetime
import logging
import random
import time

# IMPORTATION THIRD PARTY
import pytest
import urllib3

# IMPORTATION INTERNAL
from degiro_connector.trading.models.trading_pb2 import (
    Order,
)

# SETUP LOGGING LEVEL
logging.basicConfig(level=logging.FATAL)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# TESTS FEATURES
@pytest.mark.trading
def test_confirm_order(mocker, trading):
    # SETUP ORDER
    order = Order(
        action=Order.Action.BUY,
        order_type=Order.OrderType.LIMIT,
        price=10,
        product_id=71981,
        size=1,
        time_type=Order.TimeType.GOOD_TILL_DAY,
    )

    # MOCK
    mock_confirmation_id = "MOCKING-CONFIRMATION-ID"
    mocker.patch(
        "degiro_connector.trading.actions.action_confirm_order.ActionConfirmOrder.connection_storage",
        mocker.Mock(session_id="MOCKING-SESSION"),
    )

    mock_response_raw = mocker.Mock()
    mock_response_raw.json.return_value = {
        "data": {
            "orderId": "MOCKING-ORDER-ID",
        }
    }
    mocker.patch(
        "degiro_connector.trading.actions.action_confirm_order.requests.Session.send",
        return_value=mock_response_raw,
    )

    # FETCH DATA
    confirmation_response = trading.confirm_order(
        confirmation_id=mock_confirmation_id,
        order=order,
    )

    # CHECK DATA
    assert isinstance(confirmation_response, Order.ConfirmationResponse)
    assert isinstance(confirmation_response.orderId, str)
