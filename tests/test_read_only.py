import pytest
import requests
from requests.adapters import HTTPAdapter

from degiro_connector.core.constants import urls
from degiro_connector.core.exceptions import ActionDisabledError
from degiro_connector.trading.api import API as TradingAPI, SENSITIVE_ACTIONS
from degiro_connector.trading.models.credentials import Credentials

CREDENTIALS = Credentials(username="user", password="password")


@pytest.fixture
def sent(monkeypatch):
    """Requests that reached the transport; nothing goes over the network."""
    calls = []

    def fake_send(self, request, *args, **kwargs):
        calls.append((request.method, request.url))
        response = requests.Response()
        response.status_code = 200
        return response

    monkeypatch.setattr(HTTPAdapter, "send", fake_send)
    return calls


def test_read_only_disables_sensitive_actions():
    api = TradingAPI(credentials=CREDENTIALS, read_only=True)

    assert api.disabled_actions == SENSITIVE_ACTIONS
    assert not SENSITIVE_ACTIONS & set(api.action_list)
    for action in SENSITIVE_ACTIONS:
        with pytest.raises(ActionDisabledError):
            getattr(api, action)
    assert callable(api.get_update)
    assert callable(api.check_order)  # only validates an order, places nothing


def test_read_only_blocks_requests_before_sending(sent):
    api = TradingAPI(credentials=CREDENTIALS, read_only=True)
    session = api.session_storage.session

    for method, url in (
        ("POST", f"{urls.ORDER_CONFIRM}/abc;jsessionid=x"),
        ("PUT", f"{urls.ORDER_UPDATE}/abc;jsessionid=x"),
        ("DELETE", f"{urls.ORDER_DELETE}/abc;jsessionid=x"),
        ("POST", urls.FAVOURITES_LIST),
        ("DELETE", f"{urls.NOTES_LIST}/1"),
    ):
        with pytest.raises(ActionDisabledError):
            session.request(method, url)
    assert sent == []

    session.get(urls.FAVOURITES_LIST)  # reading stays possible
    session.post(f"{urls.ORDER_CHECK};jsessionid=x")
    assert [m for m, _ in sent] == ["GET", "POST"]


def test_disabled_actions_can_add_check_order(sent):
    api = TradingAPI(
        credentials=CREDENTIALS, read_only=True, disabled_actions={"check_order"}
    )

    with pytest.raises(ActionDisabledError):
        api.check_order
    with pytest.raises(ActionDisabledError):
        api.session_storage.session.post(f"{urls.ORDER_CHECK};jsessionid=x")
    assert sent == []


def test_single_order_action_only_blocks_its_method(sent):
    api = TradingAPI(credentials=CREDENTIALS, disabled_actions={"delete_order"})
    session = api.session_storage.session

    with pytest.raises(ActionDisabledError):
        session.delete(f"{urls.ORDER_DELETE}/abc")
    session.put(f"{urls.ORDER_UPDATE}/abc")  # same URL, other action
    assert sent == [("PUT", f"{urls.ORDER_UPDATE}/abc")]


def test_session_set_from_outside_is_blocked_too(sent):
    api = TradingAPI(credentials=CREDENTIALS, read_only=True)
    api.session_storage.session = requests.Session()

    with pytest.raises(ActionDisabledError):
        api.session_storage.session.post(f"{urls.ORDER_CONFIRM}/abc")
    assert sent == []


def test_default_keeps_everything_enabled(sent):
    api = TradingAPI(credentials=CREDENTIALS)

    assert api.disabled_actions == frozenset()
    assert SENSITIVE_ACTIONS <= set(api.action_list)
    api.session_storage.session.post(f"{urls.ORDER_CONFIRM}/abc")
    assert len(sent) == 1


def test_unknown_action_is_rejected():
    with pytest.raises(ValueError):
        TradingAPI(credentials=CREDENTIALS, disabled_actions={"place_order_typo"})
