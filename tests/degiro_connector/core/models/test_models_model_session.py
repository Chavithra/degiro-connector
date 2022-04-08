# IMPORTATIONS STANDARD
import logging
#import os
#import sys

# IMPORTATION THIRD PARTY
import pytest
import requests
from urllib3 import poolmanager
import ssl
import requests

# IMPORTATION INTERNAL
from degiro_connector.core.models.model_session import ModelSession
import degiro_connector.core.constants.urls as urls


# this adapter will use a wrong trusted CA certificate list
# SSL handshake will fail
class FaultyAdapter(requests.adapters.HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False, **pool_kwargs):
        # create context with OS default trusted CA certificate list
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ctx.check_hostname = True
        ctx.set_ciphers("DEFAULT@SECLEVEL=2")  
        ctx.verify_mode = ssl.CERT_REQUIRED
        self.poolmanager = poolmanager.PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_version=ssl.PROTOCOL_TLSv1_2,
            ssl_context=ctx,
            cert_reqs=ssl.CERT_REQUIRED,
            **pool_kwargs
        )
    def cert_verify(self, conn, url, verify, cert):
        # CERT_REQUIRED need to be repeated here if we want the certificate get verified
        conn.cert_reqs = 'CERT_REQUIRED'
        # Set the trusted CA certificate list. We assume the current directory is 'test'
        conn.ca_certs = './tests/degiro_connector/core/models/fake.pem'

# this adapter is the same as the default one in model_session.py
# however here we don't rely on the operating system default trusted CA certificate list
class SecureAdapter(requests.adapters.HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False, **pool_kwargs):
        # create context with OS default trusted CA certificate list
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ctx.check_hostname = True
        ctx.set_ciphers("DEFAULT@SECLEVEL=2")
        ctx.verify_mode = ssl.CERT_REQUIRED
        self.poolmanager = poolmanager.PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_version=ssl.PROTOCOL_TLSv1_2,
            ssl_context=ctx,
            **pool_kwargs
        )               
    def cert_verify(self, conn, url, verify, cert):
        # CERT_REQUIRED need to be repeated here if we want the certificate get verified
        conn.cert_reqs = 'CERT_REQUIRED'
        # Set the trusted CA certificate list. We assume the current directory is 'test'
        conn.ca_certs = './tests/degiro_connector/core/models/root.pem'



# SETUP LOGGING LEVEL
logging.basicConfig(level=logging.FATAL)


# TESTS FEATURES -- test default SSL connection
@pytest.mark.core
@pytest.mark.network
def test_model_session_DefaultAdapter():
    session_storage=ModelSession()  # default adapter is set by default, relying on OS trusted CA certificates
    session = session_storage.session
    url = urls.LOGIN
    payload_dict = {
        "queryParams": {},
    }
    request = requests.Request(
        method="POST",
        url=url,
        json=payload_dict,
    )
    prepped = session.prepare_request(request)
    errorName = None
    try:
        session.send(prepped)
    except Exception as e:
        errorName = type(e).__name__
    # result: errorName as None
    assert errorName is None



# TESTS FEATURES -- test SSL connection with fixed CA list
@pytest.mark.core
@pytest.mark.network
def test_model_session_valid():
    session_storage=ModelSession(adapter=SecureAdapter) 
    session = session_storage.session
    url = urls.LOGIN
    payload_dict = {
        "queryParams": {},
    }
    request = requests.Request(
        method="POST",
        url=url,
        json=payload_dict,
    )
    prepped = session.prepare_request(request)
    errorName = None
    try:
        session.send(prepped)
    except Exception as e:
        errorName = type(e).__name__
    # result: errorName as None
    assert errorName is None


# TESTS FEATURES -- test a failing SSL connection 
@pytest.mark.core
@pytest.mark.network
def test_model_session_faulty():
    session_storage=ModelSession(adapter=FaultyAdapter) 
    session = session_storage.session
    url = urls.LOGIN
    payload_dict = {
        "queryParams": {},
    }
    request = requests.Request(
        method="POST",
        url=url,
        json=payload_dict,
    )
    prepped = session.prepare_request(request)
    errorName = None
    try:
        session.send(prepped)
    except Exception as e:
        errorName = type(e).__name__
    # result: errorName as a string stating the SSL error
    assert errorName is not None
