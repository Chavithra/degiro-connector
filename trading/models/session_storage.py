import logging
import requests
import threading

class SessionStorage:
    """ Handle the Requests Session objects in a threadsafe manner. """

    @property
    def session(self)->requests.Session:
        """ Getter for the attribute : self.session
        
        Returns:
            {requests.Session} -- Current Session object.
        """

        self.logger.debug(
            'session:getter: %s',
            threading.current_thread().name
        )

        if not hasattr(self._local_storage, 'session'):
            self._local_storage.session = self.build_session()
        
        return self._local_storage.session

    @session.setter
    def session(self, session:requests.Session):
        """ Setter for the attribute : self.session

        Arguments:
            session {requests.Session} -- New Session object.
        """
        
        self.logger.debug(
            'session:setter: %s',
            threading.current_thread().name
        )
        
        self._local_storage.session = session

    def build_session(self, headers:dict=None, hooks:dict=None) -> requests.Session:
        """ Setup a requests.Session object.

        Arguments:
        headers {dict} -- Headers to used for the Session.

        Returns:
        {requests.Session} -- Session object with the right headers.
        """

        session = requests.Session()

        if isinstance(headers, dict) :
            session.headers.update(headers)
        elif isinstance(self._headers, dict):
            session.headers.update(self._headers)
        
        if isinstance(hooks, dict) :
            session.hooks.update(hooks)
        elif isinstance(self._hooks, dict):
            session.hooks.update(self._hooks)

        return session

    def reset_session(self, headers:dict=None, hooks:dict=None):
        self._local_storage.session = self.build_session(
            headers=headers,
            hooks=hooks
        )

    def __init__(self, headers:dict=None, hooks:dict=None):
        self.logger = logging.getLogger(self.__module__)
        self._local_storage = threading.local()
        
        if isinstance(headers, dict) :
            headers = dict(headers)
        
        if isinstance(hooks, dict):
            hooks = dict(hooks)

        self._headers = headers
        self._hooks = hooks