# IMPORTATIONS
import json
import logging
import pytest
import random
import time
import urllib3

from trading.api import API as TradingAPI
from trading.pb.trading_pb2 import Credentials

# SETUP LOGGING LEVEL
logging.basicConfig(level=logging.FATAL)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

@pytest.fixture
def config_dict():
    with open('config/config.json') as config_file:
        config_dict = json.load(config_file)
    
    return config_dict

@pytest.fixture
def credentials(config_dict):
    username = config_dict['username']
    password = config_dict['password']
    credentials = Credentials(
        int_account=None,
        username=username,
        password=password,
    )

    return credentials

@pytest.fixture
def trading_api(credentials):
    trading_api = TradingAPI(credentials=credentials)
    trading_api.connect()

    return trading_api

def test_session_id(trading_api):
    time.sleep(random.uniform(0, 2))

    session_id = trading_api.connection_storage.session_id

    assert isinstance(session_id, str)
    assert len(session_id) == 45