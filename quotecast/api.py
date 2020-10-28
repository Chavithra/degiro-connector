import json
import logging
import requests
import threading
import time
import urllib3

from quotecast.basic import Basic
from quotecast.models.connection_storage import  ConnectionStorage
from quotecast.pb.quotecast_pb2 import (
    Quotecast,
    Request,
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class API:
    """ Same operation then Basic but with "session_id" management.

    This class should be threadsafe.
    """

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

        self._basic = basic
    
    
    @property
    def connection_storage(self)->Basic:
        """ Getter for the attribute : self.connection_storage
        
        Returns:
            {Basic} -- Current ConnectionStorage object.
        """

        return self._connection_storage

    @connection_storage.setter
    def connection_storage(
        self,
        connection_storage:ConnectionStorage,
    ):
        """ Setter for the attribute : self.connection_storage

        Arguments:
            connection_storage {ConnectionStorage} -- New ConnectionStorage object.
        """

        self._connection_storage = connection_storage

    def __init__(
        self,
        user_token:int,
    ):
        self._logger = logging.getLogger(self.__module__)
        self._basic = Basic(user_token=user_token)
        self._connection_storage = ConnectionStorage(basic=self.basic)

    def fetch_data(self)->Quotecast:
        """
        Fetch data from the feed.

        Returns :
        dict
            response : JSON encoded string fetched from this endpoint.
            response_datetime : Datetime at which we received the response.
            request_duration : Duration of the request.
        """

        basic = self.basic
        session_id = self.connection_storage.session_id

        return basic.fetch_data(
            session_id=session_id
        )

    def subscribe(
        self,
        request:Request
    )->bool:
        """ Subscribe/unsubscribe to a feed from Degiro's QuoteCast API.
        Parameters :
        session {requests.Session}
            Session for the request.
            A new requests.Session will be generated automatically if None is passed.

        Returns :
        {bool} -- Whether or not the subscription succeeded.
        """

        basic = self.basic
        session_id = self.connection_storage.session_id

        return basic.subscribe(
            request=request,
            session_id=session_id,
        )

if __name__ == '__main__':
    # IMPORTATIONS
    import logging
    import json

    logging.basicConfig(level=logging.DEBUG)
    
    with open('config/subscription_request.json') as config_file:
        config = json.load(config_file)

    # SETUP VARIABLES
    user_token = config['user_token']
    product_id = 360015751
    label_list =[
        'LastDate',
        'LastTime',
        'LastPrice',
        'LastVolume',
    ]

    api = API(user_token=user_token)
    
    request = Request(
        action=Request.Action.SUBSCRIBE,
        product_id=product_id,
        label_list=label_list,
    )

    api.connection_storage.connect()
    api.subscribe(request=request)
    time.sleep(1)
    api.fetch_data()