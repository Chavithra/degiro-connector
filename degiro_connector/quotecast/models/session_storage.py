import logging
import requests
import threading

# FIX #61631955
# Degiro's server has a low level of security
# Which is not compatible with OpenSSL 1.1.1
# https://stackoverflow.com/questions/61631955/python-requests-ssl-error-during-requests
import ssl
from urllib3 import poolmanager


class TLSAdapter(requests.adapters.HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        """Create and initialize the urllib3 PoolManager."""
        ctx = ssl.create_default_context()
        ctx.set_ciphers('DEFAULT@SECLEVEL=1')

        # FIX #33770129
        # https://stackoverflow.com/questions/33770129/how-do-i-disable-the-ssl-check-in-python-3-x
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        self.poolmanager = poolmanager.PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_version=ssl.PROTOCOL_TLS,
            ssl_context=ctx,
        )


class SessionStorage:
    """ Handle the Requests Session objects in a threadsafe manner. """

    @property
    def session(self) -> requests.Session:
        self.__logger.debug(
            'session:getter: %s',
            threading.current_thread().name
        )

        if not hasattr(self.__local_storage, 'session'):
            self.__local_storage.session = self.build_session()

        return self.__local_storage.session

    @session.setter
    def session(self, session: requests.Session):
        self.__logger.debug(
            'session:setter: %s',
            threading.current_thread().name
        )

        self.__local_storage.session = session

    def build_session(
        self,
        headers: dict = None,
        hooks: dict = None,
    ) -> requests.Session:
        """
        Args:
            headers (dict, optional):
                Headers to used for the Session.
                Defaults to None.
            hooks (dict, optional):
                Hooks for the Session.
                Defaults to None.

        Returns:
            requests.Session:
                Session object with the right headers and hooks.
        """

        session = requests.Session()

        # FIX #61631955
        session.mount('https://', TLSAdapter())

        if isinstance(headers, dict):
            session.headers.update(headers)
        elif isinstance(self.__headers, dict):
            session.headers.update(self.__headers)

        if isinstance(hooks, dict):
            session.hooks.update(hooks)
        elif isinstance(self.__hooks, dict):
            session.hooks.update(self.__hooks)

        return session

    def reset_session(self, headers: dict = None, hooks: dict = None):
        self.__local_storage.session = self.build_session(
            headers=headers,
            hooks=hooks
        )

    def __init__(self, headers: dict = None, hooks: dict = None):
        self.__logger = logging.getLogger(self.__module__)
        self.__local_storage = threading.local()

        if isinstance(headers, dict):
            headers = dict(headers)

        if isinstance(hooks, dict):
            hooks = dict(hooks)

        self.__headers = headers
        self.__hooks = hooks
