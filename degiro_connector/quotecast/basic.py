import logging
import degiro_connector.quotecast.utilities as utilities
import urllib3

from degiro_connector.quotecast.constants.headers import Headers
from degiro_connector.quotecast.models.session_storage import SessionStorage
from degiro_connector.quotecast.pb.quotecast_pb2 import Chart, Quotecast
from typing import Dict

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Basic:
    """ Tools to consume Degiro's QuoteCast API.

    Same operations than "utilities" but with automatic management of :
        * user_token
        * requests.Session
        * logging.Logger

    This class should be threadsafe.
    """

    @staticmethod
    def build_session_storage() -> SessionStorage:
        return SessionStorage(
            headers=Headers.get_headers(),
            hooks=None,
        )

    @property
    def session_storage(self) -> SessionStorage:
        return self._session_storage

    @session_storage.setter
    def session_storage(self, session_storage: SessionStorage):
        self._session_storage = session_storage

    @property
    def user_token(self) -> int:
        return self._user_token

    def __init__(self, user_token: int, session_storage=None):
        if session_storage is None:
            session_storage = self.build_session_storage()

        self._logger = logging.getLogger(self.__module__)
        self._user_token = user_token
        self._session_storage = session_storage

    def fetch_data(self, session_id: str) -> Quotecast:
        logger = self._logger
        session = self._session_storage.session

        return utilities.fetch_data(
            session_id=session_id,
            session=session,
            logger=logger,
        )

    def get_session_id(self) -> str:
        logger = self._logger
        session = self._session_storage.session
        user_token = self._user_token

        return utilities.get_session_id(
            user_token=user_token,
            session=session,
            logger=logger
        )

    def subscribe(
        self,
        request: Quotecast.Request,
        session_id: str,
    ) -> bool:
        logger = self._logger
        session = self._session_storage.session

        return utilities.subscribe(
            request=request,
            session_id=session_id,
            session=session,
            logger=logger,
        )

    def get_chart(
        self,
        request: Chart.Request,
        override: Dict[str, str] = None,
        raw: bool = False,
    ) -> Chart:
        logger = self._logger
        session = self._session_storage.session
        user_token = self._user_token

        return utilities.get_chart(
            request=request,
            user_token=user_token,
            override=override,
            raw=raw,
            session=session,
            logger=logger,
        )


if __name__ == '__main__':
    # IMPORTATIONS
    import json
    import time

    # SETUP LOGS
    logging.basicConfig(level=logging.DEBUG)

    # SETUP CREDENTIALS
    with open('config/subscription_request.json') as config_file:
        config = json.load(config_file)
    user_token = config['user_token']

    # SETUP API
    basic = Basic(user_token=user_token)

    # SETUP REQUEST
    request = Quotecast.Request()
    request.subscriptions['360015751'].extend([
        'LastDate',
        'LastTime',
        'LastPrice',
        'LastVolume',
    ])

    # CONNECT
    session_id = basic.get_session_id()

    # SUBSCRIBE
    basic.subscribe(request=request, session_id=session_id)

    # FETCH DATA
    time.sleep(1)
    basic.fetch_data(session_id=session_id)
