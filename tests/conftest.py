# IMPORTATION STANDARD
import json
import os
from typing import Dict, Union

# IMPORTATION THIRD PARTY
import pytest

# IMPORTATION INTERNAL
from degiro_connector.trading.pb.trading_pb2 import Credentials

CONFIG_FILE = "config/config.json"

def pytest_addoption(parser):
    # QUOTECAST CREDENTIALS
    parser.addoption(
        "--user-token",
        action="store",
        default=None,
        help="Quotecast credentials : `user_token`",
        type=int,
    )

    # TRADING CREDENTIALS
    parser.addoption(
        "--int-account",
        action="store",
        default=None,
        help="Trading credentials : `int_account`",
        type=int,
    )

    parser.addoption(
        "--username",
        action="store",
        default=None,
        help="Trading credentials : `username`",
        type=str,
    )

    parser.addoption(
        "--password",
        action="store",
        default=None,
        help="Trading credentials : `password`",
        type=str,
    )

    parser.addoption(
        "--totp-secret-key",
        action="store",
        default=None,
        help="Trading credentials : `totp_secret_key`",
        type=str,
    )

    parser.addoption(
        "--one-time-password",
        action="store",
        default=None,
        help="Trading credentials : `one_time_password`",
        type=int,
    )


# SETUP FIXTURES
@pytest.fixture(scope='module')
def config() -> Dict[str, Union[int, str]]:
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE) as config_file:
            config_dict = json.load(config_file)
    else:
        config_dict = None

    return config_dict


@pytest.fixture(scope='module')
def user_token(config, request) -> int:
    """ Get `--user-token` argument from `CONFIG_FILE` or CLI.

    Args:
        config: `config` fixture.
        request: Pytest `request` fixture.

    Returns:
        int: Quotecast API's credential : `user_token`.
    """

    if config is not None :
        return config["user_token"]
    else:
        return request.config.getoption("--user-token")


@pytest.fixture(scope='module')
def credentials(config, request) -> Credentials:
    """ Get `--user-token` argument from `CONFIG_FILE` or CLI.

    Args:
        config: `config` fixture.
        request: Pytest `request` fixture.

    Returns:
        Credentials: Trading API's credentials.
    """

    if config is not None :
        int_account = config.get("int_account")
        username = config.get("username")
        password = config.get("password")
        totp_secret_key = config.get("totp_secret_key")
        one_time_password = config.get("one_time_password")
    else:
        int_account = request.config.getoption("--int-account")
        username = request.config.getoption("--username")
        password = request.config.getoption("--password")
        totp_secret_key = request.config.getoption("--totp-secret-key")
        one_time_password = request.config.getoption("--one-time-password")

    credentials = Credentials(
        int_account=int_account,
        username=username,
        password=password,
        totp_secret_key=totp_secret_key,
        one_time_password=one_time_password,
    )

    return credentials
