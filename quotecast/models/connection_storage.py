import logging
import requests
import time
import threading

from quotecast.api import Basic
from quotecast.constants.headers import Headers
from quotecast.models.session_storage import SessionStorage
from wrapt.decorators import synchronized

class ConnectionStorage:
    @property
    def basic(self)->Basic:
        """ Getter for the attribute : self.basic
        
        Returns:
            {Basic} -- Current Basic object.
        """

        return self._basic

    @basic.setter
    def basic(self, basic:Basic):
        """ Setter for the attribute : self.basic

        Arguments:
            basic {Basic} -- New Basic object.
        """

        basic.session_storage = self.build_session_storage()

        self._basic = basic

    @property
    @synchronized
    def session_id(self) -> str:
        """ Getter for the attribute : self.session_id
        
        Returns:
            {str} -- Copy of the session id.
        """

        if not hasattr(self, '_session_id'):
            raise ConnectionAbortedError('Connection required.')

        if self.is_timeout_expired():
            raise TimeoutError('Connection have probably expired')

        return self._session_id

    @session_id.setter
    @synchronized
    def session_id(self, session_id:str):
        """ Setter for the attribute setter : self.session_id

        Arguments:
            session {requests.Session} -- New Session object.
        """

        self._session_id = session_id

    def build_session_storage(self)->SessionStorage:
        headers = Headers.get_headers()
        hooks = {'response':[self.response_hook]}

        session_storage = SessionStorage(
            headers=headers,
            hooks=hooks
        )

        return session_storage

    def __init__(self, basic:Basic, session_timeout=15):
        self.basic = basic
        self.session_timeout = session_timeout
        self._last_success = 0

    @synchronized
    def is_timeout_expired(self):
        if not hasattr(self, '_last_success') :
            return False

        return (time.monotonic() - self._last_success) > self.session_timeout

    @synchronized
    def response_hook(self, response, *args, **kwargs):
        """ This hook will intercept all the "requests.Response". """

        timestamp = time.monotonic()
        status_code = response.status_code

        if self._last_success < timestamp \
        and status_code == 200:
            self._last_success = timestamp

    @synchronized
    def connect(self):
        basic = self.basic
        self.session_id = basic.get_session_id()