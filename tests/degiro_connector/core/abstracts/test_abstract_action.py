# IMPORTATIONS STANDARD
import logging

# IMPORTATION THIRD PARTY
import pytest
import requests

# IMPORTATION INTERNAL
from degiro_connector.core.abstracts.abstract_action import AbstractAction

# SETUP LOGGING LEVEL
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
