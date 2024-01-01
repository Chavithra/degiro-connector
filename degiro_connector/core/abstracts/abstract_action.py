import abc
import logging
import requests
from inspect import ismethod


from degiro_connector.core.models.model_connection import ModelConnection
from degiro_connector.core.models.model_session import ModelSession


class AbstractAction(abc.ABC):
    # COMMENTING @final : FOR COMPATIBILITY WITH PYTHON 3.7
    # @final
    @staticmethod
    def build_logger() -> logging.Logger:
        return logging.getLogger(__name__)

    # @final
    @staticmethod
    def build_session(headers: dict[str, str] | None = None) -> requests.Session:
        return ModelSession.build_session()

    # @final
    @property
    def credentials(self):
        return self._credentials

    # @final
    @property
    def connection_storage(self):
        return self._connection_storage

    # @final
    @property
    def logger(self):
        return self._logger

    # @final
    @property
    def session_storage(self):
        return self._session_storage

    # @final
    def __init__(
        self,
        credentials,
        connection_storage: ModelConnection,
        logger: logging.Logger | None = None,
        session_storage: ModelSession = None,
        *args,
        **kwargs,
    ):
        # Each action implement a `call` method.
        # This `call` method can have it's own set of *args and **kwargs
        assert hasattr(self, "call") and ismethod(getattr(self, "call"))

        self._credentials = credentials
        self._connection_storage = connection_storage
        self._logger = logger or logging.getLogger(self.__module__)
        self._session_storage = session_storage or ModelSession(
            hooks=self._connection_storage.build_hooks(),
            ssl_check=True,
        )

        self.post_init(*args, **kwargs)

    # @final
    def __call__(self, *args, **kwargs):
        return self.call(*args, **kwargs)

    def post_init(self, *args, **kwargs):
        pass
