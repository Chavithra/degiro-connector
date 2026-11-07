from pathlib import Path
import runpy
from unittest.mock import Mock

import pytest
import requests

from degiro_connector.trading.actions.action_get_company_logo import (
    ActionGetCompanyLogo,
)
from degiro_connector.trading.actions.action_get_company_logo_url import (
    ActionGetCompanyLogoUrl,
)
from degiro_connector.trading.api import API
from degiro_connector.trading.models.credentials import Credentials
from degiro_connector.trading.models.company_logo import CompanyLogo

pytestmark = pytest.mark.trading


@pytest.mark.parametrize(
    "product_isin",
    [
        pytest.param("US0378331005", id="apple"),
        pytest.param("US5949181045", id="microsoft"),
        pytest.param("US88160R1014", id="tesla"),
        pytest.param("US30303M1027", id="meta"),
    ],
)
def test_company_logo_url(product_isin, mocker):
    send = mocker.patch("requests.Session.send")

    assert ActionGetCompanyLogoUrl.get_company_logo_url(product_isin) == (
        f"https://trader.degiro.nl/logos/api/logos/isin/{product_isin}"
    )
    send.assert_not_called()


def test_company_logo_url_encodes_path_characters():
    assert ActionGetCompanyLogoUrl.get_company_logo_url("ISIN/with?query#") == (
        "https://trader.degiro.nl/logos/api/logos/isin/ISIN%2Fwith%3Fquery%23"
    )


def test_company_logo_bytes_with_supplied_session():
    response = requests.Response()
    response.status_code = 200
    response._content = b"\x89PNG\r\n\x1a\n\x00\xff"
    session = Mock(spec=requests.Session)
    session.get.return_value = response

    assert (
        ActionGetCompanyLogo.get_company_logo(
            "US0378331005", session=session, timeout=7
        )
        == response.content
    )
    session.get.assert_called_once_with(
        "https://trader.degiro.nl/logos/api/logos/isin/US0378331005", timeout=7
    )
    session.close.assert_not_called()


@pytest.mark.parametrize(
    "content_type, expected_type, extension",
    [
        ("image/svg+xml", "image/svg+xml", ".svg"),
        ("IMAGE/SVG+XML; charset=utf-8", "image/svg+xml", ".svg"),
        ("image/png", "image/png", ".png"),
        ("image/jpeg", "image/jpeg", ".jpg"),
        ("image/webp", "image/webp", ".webp"),
        ("image/x-unknown-format", "image/x-unknown-format", ".bin"),
        ("application/octet-stream", "application/octet-stream", ".bin"),
        ("", "application/octet-stream", ".bin"),
        (None, "application/octet-stream", ".bin"),
    ],
)
def test_company_logo_metadata(content_type, expected_type, extension):
    response = requests.Response()
    response.status_code = 200
    response._content = b'<svg xmlns="http://www.w3.org/2000/svg"/>'
    if content_type is not None:
        response.headers["Content-Type"] = content_type
    session = Mock(spec=requests.Session)
    session.get.return_value = response

    logo = ActionGetCompanyLogo.get_company_logo(
        "US0378331005", session=session, include_metadata=True
    )

    assert isinstance(logo, CompanyLogo)
    assert logo.content == response.content
    assert logo.content_type == expected_type
    assert logo.extension == extension


@pytest.mark.parametrize("include_metadata", [False, True])
@pytest.mark.parametrize(
    "content_type, content",
    [
        ("text/html; charset=utf-8", b"<html>Service unavailable</html>"),
        ("APPLICATION/JSON", b'{"error":"logo unavailable"}'),
    ],
)
def test_company_logo_rejects_non_image_responses(
    content_type, content, include_metadata, mocker
):
    response = requests.Response()
    response.status_code = 200
    response.headers["Content-Type"] = content_type
    response._content = content
    session = Mock(spec=requests.Session)
    session.get.return_value = response
    mocker.patch.object(ActionGetCompanyLogo, "build_session", return_value=session)
    logger = Mock()

    assert (
        ActionGetCompanyLogo.get_company_logo(
            "US0378331005", logger=logger, include_metadata=include_metadata
        )
        is None
    )
    logger.error.assert_called_once()
    session.close.assert_called_once_with()


def test_example_saves_svg_with_extension(tmp_path, monkeypatch, mocker):
    example = Path(__file__).resolve().parents[4] / "examples/trading/company_logo.py"
    response = requests.Response()
    response.status_code = 200
    response.headers["Content-Type"] = "image/svg+xml; charset=utf-8"
    response._content = b'<svg xmlns="http://www.w3.org/2000/svg"/>'
    mocker.patch("requests.Session.send", return_value=response)
    monkeypatch.chdir(tmp_path)

    runpy.run_path(str(example), run_name="__main__")

    assert (tmp_path / "apple-logo.svg").read_bytes() == response.content
    assert not (tmp_path / "apple-logo").exists()


@pytest.mark.parametrize("status_code", [404, 500])
def test_company_logo_http_error(status_code):
    response = requests.Response()
    response.status_code = status_code
    response._content = b"Logo unavailable"
    session = Mock(spec=requests.Session)
    session.get.return_value = response

    assert (
        ActionGetCompanyLogo.get_company_logo("US0378331005", session=session) is None
    )


@pytest.mark.parametrize("error", [requests.Timeout, requests.ConnectionError])
def test_company_logo_transport_error_closes_owned_session(error, mocker):
    session = Mock(spec=requests.Session)
    session.get.side_effect = error("Request failed")
    mocker.patch.object(ActionGetCompanyLogo, "build_session", return_value=session)

    assert ActionGetCompanyLogo.get_company_logo("US0378331005") is None
    session.close.assert_called_once_with()


@pytest.mark.parametrize("preload", [False, True])
@pytest.mark.parametrize("include_metadata", [False, True])
def test_company_logo_actions_without_connection(preload, include_metadata, mocker):
    # A trading API can expose both actions before connect() is called.
    api = API(
        credentials=Credentials(username="unused", password="unused"),
        preload=preload,
    )
    response = requests.Response()
    response.status_code = 200
    response._content = b"\x00\xffimage bytes"
    send = mocker.patch("requests.Session.send", return_value=response)
    close = mocker.spy(requests.Session, "close")

    assert api.get_company_logo_url("US0378331005") == (
        "https://trader.degiro.nl/logos/api/logos/isin/US0378331005"
    )
    send.assert_not_called()
    logo = api.get_company_logo("US0378331005", include_metadata=include_metadata)
    if include_metadata:
        assert isinstance(logo, CompanyLogo)
        assert logo.content == response.content
    else:
        assert logo == response.content

    request = send.call_args.args[0]
    assert request.method == "GET"
    assert request.url == api.get_company_logo_url("US0378331005")
    assert "Cookie" not in request.headers
    assert "Authorization" not in request.headers
    assert send.call_args.kwargs["timeout"] == 30
    close.assert_called_once()
