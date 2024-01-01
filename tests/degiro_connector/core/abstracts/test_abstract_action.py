# IMPORTATIONS STANDARD
import logging

import pytest
import requests

from degiro_connector.core.abstracts.abstract_action import AbstractAction

logging.basicConfig(level=logging.FATAL)


# TESTS FEATURES
@pytest.mark.core
def test_build_logger():
    # SETUP
    logger = AbstractAction.build_logger()

    # CHECK
    assert isinstance(logger, logging.Logger)


# TESTS FEATURES
@pytest.mark.core
def test_build_session():
    # SETUP
    session = AbstractAction.build_session()

    # CHECK
    assert isinstance(session, requests.Session)
