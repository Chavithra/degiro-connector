import logging
import quotecast.utilities as utilities
import urllib3

from quotecast.constants.headers import Headers
from quotecast.models.session_storage import SessionStorage
from quotecast.pb.quotecast_pb2 import Quotecast, Request
from typing import Union

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
    def user_token(self)->int:
        return self._user_token

    @property
    def session_storage(self)->SessionStorage:
        return self._session_storage

    @session_storage.setter
    def session_storage(
        self,
        session_storage:SessionStorage,
    ):
        self._session_storage = session_storage

    def build_session_storage(self)->SessionStorage:
        return SessionStorage(
            headers=Headers.get_headers(),
            hooks=None,
        )

    def __init__(
        self,
        user_token:int,
        session_storage=None,
    ):
        if session_storage is None:
            session_storage = self.build_session_storage()

        self._logger = logging.getLogger(self.__module__)
        self._user_token = user_token
        self._session_storage = session_storage

    def fetch_data(
        self,
        session_id:str,
    )->Quotecast:
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

        logger = self._logger
        session = self._session_storage.session

        return utilities.fetch_data(
            session_id=session_id,
            session=session,
            logger=logger,
        )

    def get_session_id(self)->str:
        """ Get the session id necessary to :
            * Subscribe to a feed.
            * Fetch available data.
       
        Returns :
        {str} -- API's session id.
        """

        logger = self._logger
        user_token = self._user_token
        session = self._session_storage.session

        return utilities.get_session_id(
            user_token=user_token,
            session=session,
            logger=logger
        )

    def subscribe(
        self,
        request:Request,
        session_id:str,
        raw:bool=False,
    )->Union[Request, int]:
        """ Subscribe/unsubscribe to a feed from Degiro's QuoteCast API.
        Parameters :
        session_id {str} -- API's session id.

        Returns :
        {bool} -- Whether or not the subscription succeeded.
        """

        logger = self._logger
        session = self._session_storage.session
        
        return utilities.subscribe(
            request=request,
            session_id=session_id,
            raw=raw,
            session=session,
            logger=logger,
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
    #     action=Request.Action.SUBSCRIBE,
    #     product_id=product_id,
    #     label_list=label_list,
    # )
    
    # basic = Basic(user_token=user_token)
    
    # session_id = basic.get_session_id()
    # basic.subscribe(subscription_request=subscription_request, session_id=session_id)
    # data = basic.fetch_data(session_id)
    # print(json.dumps(data))