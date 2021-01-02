import logging
import urllib3

from quotecast.basic import Basic
from quotecast.models.connection_storage import  ConnectionStorage
from quotecast.pb.quotecast_pb2 import Quotecast

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class API:
    """ Tools to consume Degiro's QuoteCast API.
    
    Same operations than "Basic" but with "session_id" management.

    This class should be threadsafe.
    """

    @property
    def basic(self)->Basic:
        return self._basic
    
    @property
    def connection_storage(self)->Basic:
        return self._connection_storage

    @property
    def user_token(self)->int:
        return self._basic.user_token

    def __init__(self, user_token:int):
        self._logger = logging.getLogger(self.__module__)
        self._basic = Basic(user_token=user_token)
        self._connection_storage = ConnectionStorage(
            session_storage=self._basic.session_storage,
            connection_timeout=15,
        )

    def connect(self):
        basic = self.basic
        connection_storage = self._connection_storage
        connection_storage.session_id = basic.get_session_id()

    def fetch_data(self)->Quotecast:
        basic = self.basic
        session_id = self.connection_storage.session_id

        return basic.fetch_data(
            session_id=session_id
        )

    def subscribe(self, request:Quotecast.Request)->bool:
        basic = self.basic
        session_id = self._connection_storage.session_id

        return basic.subscribe(
            request=request,
            session_id=session_id,
        )

if __name__ == '__main__':
    # IMPORTATIONS
    import json
    import logging
    import time

    # SETUP LOGS
    logging.basicConfig(level=logging.DEBUG)

    # SETUP CREDENTIALS    
    with open('config/subscription_request.json') as config_file:
        config = json.load(config_file)
    user_token = config['user_token']

    # SETUP API
    api = API(user_token=user_token)

    # SETUP REQUEST
    request = Quotecast.Request()
    request.subscriptions['360015751'].extend([
        'LastDate',
        'LastTime',
        'LastPrice',
        'LastVolume',
    ])

    # CONNECT
    api.connect()

    # SUBSCRIBE
    api.subscribe(request=request)

    # FETCH DATA
    time.sleep(1)
    api.fetch_data()