import json
import logging
import quotecast.utilities as utilities
import requests
import threading
import time
import urllib3

from quotecast.constants import Headers
from quotecast.models.sessions_storage import SessionsStorage
from quotecast.pb.quotecast_pb2 import (
    Action,
    Credentials,
    RawResponse,
    SubscriptionRequest
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Basic:
    """ This class contains the tool necessary to exchange with Degiro's QuoteCast API.
    
    This class should be threadsafe.

    Using this class one can :
        * Create a session
        * Subscribe to QuoteCast about financial products available from Degiro's website
        * Fetch the data stream of the product to which one subscribed

    Attributes :
    config_api {ConfigAPI} -- Contains parameters required to call the API.

    logger {logging.Logger} -- The information logging system.
    """

    @property
    def credentials(self)->Credentials:
        return self._credentials

    @property
    def sessions_storage(self)->SessionsStorage:
        return self._sessions_storage

    @sessions_storage.setter
    def sessions_storage(self, sessions_storage:SessionsStorage):
        self._sessions_storage = sessions_storage

    def build_sessions_storage(self)->SessionsStorage:
        return SessionsStorage(
            headers=Headers.get_headers(),
            hooks=None
        )

    def __init__(self, credentials:Credentials, sessions_storage=None):
        if sessions_storage is None:
            sessions_storage = self.build_sessions_storage()

        self.logger = logging.getLogger(self.__module__)
        self._credentials = credentials
        self._sessions_storage = sessions_storage

    def fetch_data(
            self,
            session_id:str,
        )->RawResponse:
        """
        Fetch data from the feed.

        Parameters :
        session_id {str} -- API's session id.

        Returns :
        dict
            response : JSON encoded string fetched from this endpoint.
            response_datetime : Datetime at which we received the response.
            request_duration : Duration of the request.
        """

        logger = self.logger
        session = self.sessions_storage.session

        return utilities.fetch_data(
            session_id=session_id,
            session=session,
            logger=logger
        )

    def get_session_id(self)->str:
        """ Get the session id necessary to :
            * Subscribe to a feed.
            * Fetch available data.
       
        Returns :
        {str} -- API's session id.
        """

        logger = self.logger
        credentials = self.credentials
        session = self.sessions_storage.session

        return utilities.get_session_id(
            credentials=credentials,
            session=session,
            logger=logger
        )

    def subscribe(self,
            subscription_request:SubscriptionRequest,
            session_id:str
        )->bool:
        """ Subscribe/unsubscribe to a feed from Degiro's QuoteCast API.
        Parameters :
        session_id {str} -- API's session id.

        Returns :
        {bool} -- Whether or not the subscription succeeded.
        """

        logger = self.logger
        session = self.sessions_storage.session
        
        return utilities.subscribe(
            subscription_request=subscription_request,
            session_id=session_id,
            session=session,
            logger=logger
        )

if __name__ == '__main__':
    import logging
    import json

    from quotecast.api import API
    from queue import Queue

    logging.basicConfig(level=logging.DEBUG)
    
    with open('subscription_request.json') as config_file:
        config = json.load(config_file)

    # Parameters required for testing
    user_token = config['user_token']
    product_id = 350000520
    label_list =[
        'LastDate',
        'LastTime',
        'LastPrice',
        'LastVolume',
    ]


    # subscription_request = SubscriptionRequest(
    #     action=SubscriptionRequest.Action.SUBSCRIBE,
    #     product_id=product_id,
    #     label_list=label_list
    # )
    
    # basic = Basic(Credentials(user_token=user_token))
    
    # session_id = basic.get_session_id()
    # basic.subscribe(subscription_request=subscription_request, session_id=session_id)
    # data = basic.fetch_data(session_id)
    # print(json.dumps(data))