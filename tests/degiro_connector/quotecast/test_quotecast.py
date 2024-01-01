# IMPORTATIONS STANDARD
import logging
import random
import time

import pytest
import urllib3

import degiro_connector.core.helpers.pb_handler as pb_handler
from degiro_connector.quotecast.api import API as QuotecastAPI
from degiro_connector.quotecast.models.quotecast_parser import QuotecastParser
from degiro_connector.quotecast.models.quotecast_pb2 import Chart, Quotecast

# SETUP LOGGING
logging.basicConfig(level=logging.FATAL)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
