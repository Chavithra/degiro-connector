import logging
import requests
import time
from threading import Event

from wrapt.decorators import synchronized


class ModelConnection:
    @property
    def connected(self) -> Event:
        return self.__connected

    @property
    def timeout(self) -> int:
        return self.__timeout

    @property  # type: ignore
    @synchronized
    def session_id(self) -> str:
        if not self.__session_id:
            raise ConnectionError("Connection required.")

        if self.is_timeout_expired():
            self.__connected.clear()
            raise TimeoutError("Connection has probably expired.")

        return self.__session_id

    @session_id.setter  # type: ignore
    @synchronized
    def session_id(self, session_id: str):
        if session_id:
            self.__session_id = session_id
            self.__connected.set()
        else:
            self.__session_id = session_id
            self.__connected.clear()

    def __init__(
        self,
        timeout: int,  # quotecast : 15s / trading: 1800s
    ):
        self.__timeout = timeout

        self.__connected = Event()
        self.__last_success = 0
        self.__logger = logging.getLogger(self.__module__)
        self.__session_id = ""

    @synchronized
    def is_timeout_expired(self):
        if not self.__last_success:
            return False

        return (time.monotonic() - self.__last_success) > self.__timeout

    @synchronized
    def response_hook(self, response, *args, **kwargs):
        """This hook will intercept all the "requests.Response"."""

        timestamp = time.monotonic()
        status_code = response.status_code

        if self.__last_success < timestamp and status_code == 200:
            self.__last_success = timestamp

    def build_hooks(self):
        return {"response": [self.response_hook]}

    def setup_hooks(self, session: requests.Session):
        session.hooks.update(self.build_hooks())
