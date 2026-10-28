import logging
import threading
from typing import Iterable

import requests
from requests.adapters import HTTPAdapter

import degiro_connector.core.constants.headers as default_headers
from degiro_connector.core.exceptions import ActionDisabledError

# (HTTP methods, URL prefix): requests matching one of these are refused before being sent
BlockedRequest = tuple[frozenset[str], str]


class BlockingAdapter(HTTPAdapter):
    """Transport adapter refusing blocked requests, whatever code path built them."""

    def __init__(self, blocked_requests: Iterable[BlockedRequest], **kwargs):
        self.blocked_requests = tuple(blocked_requests)
        super().__init__(**kwargs)

    def send(self, request, *args, **kwargs):
        for methods, url_prefix in self.blocked_requests:
            if request.method in methods and request.url.startswith(url_prefix):
                raise ActionDisabledError(
                    f"Request blocked: {request.method} {url_prefix}"
                )

        return super().send(request, *args, **kwargs)


class ModelSession:
    """Handle the Requests Session objects in a threadsafe manner."""

    @staticmethod
    def build_session(
        headers: dict | None = None,
        hooks: dict | None = None,
        blocked_requests: Iterable[BlockedRequest] | None = None,
    ) -> requests.Session:
        """Setup a "requests.Session" object.
        Args:
            headers (dict, optional):
                Headers to used for the Session.
                Defaults to None.
            hooks (dict, optional):
                Hooks for the Session.
                Defaults to None.
            blocked_requests (Iterable[BlockedRequest], optional):
                (HTTP methods, URL prefix) pairs refused before being sent.
                Defaults to None.

        Returns:
            requests.Session:
                Session object with the right headers and hooks.
        """

        session = requests.Session()

        if isinstance(headers, dict):
            session.headers.update(headers)
        else:
            session.headers.update(default_headers.HEADERS)

        if isinstance(hooks, dict):
            session.hooks.update(hooks)

        if blocked_requests:
            adapter = BlockingAdapter(blocked_requests=blocked_requests)
            session.mount("https://", adapter)
            session.mount("http://", adapter)

        return session

    @property
    def session(self) -> requests.Session:
        self.__logger.debug("session:getter: %s", threading.current_thread().name)

        if not hasattr(self.__local_storage, "session"):
            self.__local_storage.session = self.build_session(
                headers=self.__headers,
                hooks=self.__hooks,
                blocked_requests=self.__blocked_requests,
            )

        return self.__local_storage.session

    @session.setter
    def session(self, session: requests.Session):
        self.__logger.debug("session:setter: %s", threading.current_thread().name)

        # a session given from outside is blocked the same way
        if self.__blocked_requests:
            adapter = BlockingAdapter(blocked_requests=self.__blocked_requests)
            session.mount("https://", adapter)
            session.mount("http://", adapter)

        self.__local_storage.session = session

    def reset_session(
        self,
        headers: dict | None = None,
        hooks: dict | None = None,
    ):
        self.__local_storage.session = self.build_session(
            headers=headers,
            hooks=hooks,
            blocked_requests=self.__blocked_requests,
        )

    def __init__(
        self,
        headers: dict | None = None,
        hooks: dict | None = None,
        blocked_requests: Iterable[BlockedRequest] | None = None,
    ):
        self.__logger = logging.getLogger(self.__module__)
        self.__local_storage = threading.local()
        self.__blocked_requests = tuple(blocked_requests or ())

        if isinstance(headers, dict):
            headers = dict(headers)

        if isinstance(hooks, dict):
            hooks = dict(hooks)

        self.__headers = headers
        self.__hooks = hooks
