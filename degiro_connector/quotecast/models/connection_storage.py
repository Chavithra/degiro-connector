import logging
import requests
import time

from degiro_connector.quotecast.models.session_storage import SessionStorage
from threading import Event
from wrapt.decorators import synchronized


class ConnectionStorage:
    @property
    def connected(self) -> Event:
        return self.__connected

    @property
    def connection_timeout(self) -> int:
        return self.__connection_timeout

    @property
    @synchronized
    def session_id(self) -> str:
        if not self.__session_id:
            raise ConnectionError('Connection required.')

        if self.is_timeout_expired():
            self.__connected.clear()
            raise TimeoutError('Connection has probably expired.')

        return self.__session_id

    @session_id.setter
    @synchronized
    def session_id(self, session_id: str):
        if session_id:
            self.__session_id = session_id
            self.__connected.set()
        else:
            self.__session_id = session_id
            self.__connected.clear()

    @property
    def session_storage(self) -> SessionStorage:
        return self.__session_storage

    def __init__(
        self,
        connection_timeout: int = 15,
    ):
        self.__connection_timeout = connection_timeout

        self.__connected = Event()
        self.__last_success = 0
        self.__logger = logging.getLogger(self.__module__)
        self.__session_id = ''

    @synchronized
    def is_timeout_expired(self):
        if not self.__last_success:
            return False

        return \
            (time.monotonic() - self.__last_success) \
            > self.__connection_timeout

    @synchronized
    def response_hook(self, response, *args, **kwargs):
        """ This hook will intercept all the "requests.Response". """

        timestamp = time.monotonic()
        status_code = response.status_code

        if self.__last_success < timestamp and status_code == 200:
            self.__last_success = timestamp

    def setup_hooks(self, session: requests.Session):
        hooks = {'response': [self.response_hook]}
        session.hooks.update(hooks)
