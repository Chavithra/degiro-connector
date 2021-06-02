import logging
import requests
import threading


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
