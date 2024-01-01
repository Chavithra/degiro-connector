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
def test_check_order(mocker, trading):
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
    mocker.patch(
        "degiro_connector.trading.actions.action_check_order.ActionCheckOrder.connection_storage",
        mocker.Mock(session_id="MOCKING-SESSION"),
    )

    mock_response_raw = mocker.Mock()
    mock_response_raw.json.return_value = {
        "data": {
            "confirmationId": "MOCKING-CONFIRMATION-ID",
            "free_space_new": 1.23,
            "transactionFees": [
                {"id": "3", "amount": 1.23, "currency": "EUR"},
                {"id": "2", "amount": 1.23, "currency": "USD"},
            ],
            "transactionOppositeFees": [
                {"id": "3", "amount": 1.23, "currency": "EUR"},
                {"id": "2", "amount": 1.23, "currency": "USD"},
            ],
            "transactionAutoFxSurcharges": [
                {"id": "2", "amount": 1.23, "currency": "EUR"},
                {"id": "T", "amount": 1.23, "currency": "EUR"},
            ],
            "transactionAutoFxOppositeSurcharges": [
                {"id": "2", "amount": 1.23, "currency": "EUR"},
                {"id": "T", "amount": -1.23, "currency": "EUR"},
            ],
            "autoFxConversionRate": 1.23,
        }
    }
    mocker.patch(
        "degiro_connector.trading.actions.action_check_order.requests.Session.send",
        return_value=mock_response_raw,
    )

    # FETCH DATA
    checking_response = trading.check_order(order=order)

    # CHECK DATA
    assert isinstance(checking_response, Order.CheckingResponse)
    assert isinstance(checking_response.confirmation_id, str)
