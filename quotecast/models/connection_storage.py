import logging
import requests
import time

from quotecast.constants.headers import Headers
from quotecast.models.session_storage import SessionStorage
from threading import Event
from wrapt.decorators import synchronized

class ConnectionStorage:
    
    @property
    def connected(self)->Event:
        return self.__connected

    @property
    def connection_timeout(self)->int:
        return self.__connection_timeout

    @property
    @synchronized
    def session_id(self) -> str:
        if not self.__session_id:
            raise ConnectionError('Connection required.')

        if self.is_timeout_expired():
            raise TimeoutError('Connection has probably expired.')
            self.__connected.clear()

        return self.__session_id

    @session_id.setter
    @synchronized
    def session_id(self, session_id:str):
        if session_id:
            self.__session_id = session_id
            self.__connected.set()

    @property
    def session_storage(self)->SessionStorage:
        return self.__session_storage

    def __init__(
        self,
        session_storage:SessionStorage,
        connection_timeout:int=15,
    ):
        self.__session_storage = session_storage
        self.__connection_timeout = connection_timeout

        self.__connected = Event()
        self.__last_success = 0
        self.__session_id = ''

        self.setup_hooks()

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

    def setup_hooks(self):
        hooks = {'response':[self.response_hook]}
        self.__session_storage.session.hooks.update(hooks)