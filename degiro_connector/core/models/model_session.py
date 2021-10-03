# IMPORTATION STANDARD
import logging
import threading

# IMPORTATION THIRD PARTY
import requests
import ssl
import urllib3
from urllib3 import poolmanager

# IMPORTATION INTERNAL
import degiro_connector.core.constants.headers as default_headers

# DISABLE WARNINGS
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class TLSAdapter(requests.adapters.HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        """Create and initialize the urllib3 PoolManager."""
        ctx = ssl.create_default_context()
        ctx.set_ciphers("DEFAULT@SECLEVEL=1")

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


class ModelSession:
    """Handle the Requests Session objects in a threadsafe manner."""

    @staticmethod
    def build_session(
        headers: dict = None,
        hooks: dict = None,
        ssl_check: bool = False,
    ) -> requests.Session:
        """Setup a "requests.Session" object.
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
        # Degiro's server has a low level of security
        # Which is not compatible with OpenSSL 1.1.1
        # https://stackoverflow.com/questions/61631955/python-requests-ssl-error-during-requests
        if ssl_check is False:
            session.mount("https://", TLSAdapter())

        if isinstance(headers, dict):
            session.headers.update(headers)
        else:
            session.headers.update(default_headers.HEADERS)

        if isinstance(hooks, dict):
            session.hooks.update(hooks)

        return session

    @property
    def session(self) -> requests.Session:
        self.__logger.debug("session:getter: %s", threading.current_thread().name)

        if not hasattr(self.__local_storage, "session"):
            self.__local_storage.session = self.build_session(
                headers=self.__headers,
                hooks=self.__hooks,
                ssl_check=self.__ssl_check,
            )

        return self.__local_storage.session

    @session.setter
    def session(self, session: requests.Session):
        self.__logger.debug("session:setter: %s", threading.current_thread().name)

        self.__local_storage.session = session

    def reset_session(
        self,
        headers: dict = None,
        hooks: dict = None,
        ssl_check: bool = False,
    ):
        self.__local_storage.session = self.build_session(
            headers=headers,
            hooks=hooks,
            ssl_check=ssl_check,
        )

    def __init__(
        self,
        headers: dict = None,
        hooks: dict = None,
        ssl_check: bool = False,
    ):
        self.__logger = logging.getLogger(self.__module__)
        self.__local_storage = threading.local()

        if isinstance(headers, dict):
            headers = dict(headers)

        if isinstance(hooks, dict):
            hooks = dict(hooks)

        self.__headers = headers
        self.__hooks = hooks
        self.__ssl_check = ssl_check
