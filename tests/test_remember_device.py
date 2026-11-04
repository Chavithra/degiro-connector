import json

import pytest
import requests
from requests.adapters import HTTPAdapter

from degiro_connector.core.constants import urls
from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.models.credentials import Credentials

TOKENS = [{"token": "user-token", "ttl": "2026-11-27T12:03:58+01:00"}]


@pytest.fixture
def degiro(monkeypatch):
    """Fake DeGiro: records requests and answers login and remember-me."""
    sent = []

    def fake_send(self, request, *args, **kwargs):
        sent.append(request)
        response = requests.Response()
        response.status_code = 200
        response.url = request.url
        if request.url.startswith(urls.REMEMBER_ME):
            body = {"data": {"userTokens": TOKENS}}
        else:
            body = {"sessionId": "session-id", "status": 0}
        response._content = json.dumps(body).encode()
        return response

    monkeypatch.setattr(HTTPAdapter, "send", fake_send)
    return sent


def test_remember_device_returns_tokens_and_device_cookies(degiro):
    credentials = Credentials(username="user", password="password")
    api = TradingAPI(credentials=credentials)
    session = api.session_storage.session
    session.cookies.set("deviceUUID", "uuid-1", domain="trader.degiro.nl", path="/")
    session.cookies.set(
        "deviceToken", "device-token", domain="trader.degiro.nl", path="/"
    )
    session.cookies.set("JSESSIONID", "not-a-device-cookie", domain="trader.degiro.nl")

    device = api.remember_device()

    assert device.user_tokens == TOKENS
    assert device.device_cookies == {
        "deviceUUID": "uuid-1",
        "deviceToken": "device-token",
    }
    assert credentials.user_tokens == TOKENS  # ready for the next login
    assert credentials.device_cookies == device.device_cookies
    assert degiro[-1].method == "POST" and degiro[-1].url == urls.REMEMBER_ME


def test_login_sends_the_remembered_device(degiro):
    credentials = Credentials(
        username="user",
        password="password",
        user_tokens=TOKENS,
        device_cookies={"deviceUUID": "uuid-1", "deviceToken": "device-token"},
    )

    session_id = TradingAPI(credentials=credentials).connect()

    login = degiro[-1]
    body = json.loads(login.body)
    assert session_id == "session-id"
    assert login.url == urls.LOGIN
    assert body["deviceId"] == "uuid-1"  # DeGiro's device id, taken from its cookie
    assert body["userTokens"] == TOKENS
    assert "deviceToken=device-token" in login.headers["Cookie"]
    assert "deviceUUID=uuid-1" in login.headers["Cookie"]


def test_login_without_device_is_unchanged(degiro):
    TradingAPI(credentials=Credentials(username="user", password="password")).connect()

    body = json.loads(degiro[-1].body)
    assert "deviceId" not in body and "userTokens" not in body
    assert "Cookie" not in degiro[-1].headers
