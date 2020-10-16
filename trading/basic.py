import json
import logging
import threading
import time
import trading.utilities as utilities

from typing import (
    List,
    Union,
)
from trading.constants import Headers
from trading.models.sessions_storage import SessionsStorage
from trading.pb.trading_pb2 import (
    Credentials,
    Order,
    Update,
)

class Basic:
    """ Wrapper for "degiro.trading.api.utilities" module.
    
    Improvements compared to "utilities" module :
    1/ Credentials
        No need to re-enter the credentials for each function.
    2/ Sessions
        The "requests.Session" object is reuse in a thread safe manner.
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
    
    def get_session_id(self)->str:
        logger = self.logger
        credentials = self.credentials
        session = self.sessions_storage.session

        return utilities.get_session_id(
            credentials=credentials,
            session=session,
            logger=logger
        )

    def get_update(
            self, 
            request_list:Update.RequestList,
            session_id:str,
            raw:bool=False,
        ) -> str:
        logger = self.logger
        credentials = self.credentials
        session = self.sessions_storage.session

        return utilities.get_update(
            request_list=request_list,
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )

    def check_order(
            self, 
            order:Order,
            session_id:str,
            raw:bool=False,
        )->Union[Order.CheckingResponse, bool]:
        logger = self.logger
        credentials = self.credentials
        session = self.sessions_storage.session

        return utilities.check_order(
            order=order,
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )

    def confirm_order(
            self,
            confirmation_id:str,
            order:Order,
            session_id:str,
            raw:bool=False,
        )->Union[Order.ConfirmationResponse, bool]:
        logger = self.logger
        credentials = self.credentials
        session = self.sessions_storage.session

        return utilities.confirm_order(
            confirmation_id=confirmation_id,
            order=order,
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )

    def update_order(
            self, 
            order:Order,
            session_id:str,
            raw:bool=False,
        ) -> str:
        logger = self.logger
        credentials = self.credentials
        session = self.sessions_storage.session

        return utilities.update_order(
            order=order,
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )

    def delete_order(
            self,
            order_id:str,
            session_id:str,
            raw:bool=False,
        ) -> bool:
        logger = self.logger
        credentials = self.credentials
        session = self.sessions_storage.session

        return utilities.delete_order(
            order_id=order_id,
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )

if __name__ == '__main__':
    with open('config.json') as config_file:
        config = json.load(config_file)

    int_account = config['int_account']
    username = config['username']
    password = config['password']
    credentials = Credentials(
        int_account=int_account,
        username=username,
        password=password
    )
    api = Basic(credentials)

    session_id = api.get_session_id()

    # option_list = [
    #     UpdateOptions.ALERTS,
    #     UpdateOptions.CASHFUNDS,
    #     UpdateOptions.HISTORICALORDERS,
    #     UpdateOptions.ORDERS,
    #     UpdateOptions.PORTFOLIO,
    #     UpdateOptions.TOTALPORTFOLIO,
    #     UpdateOptions.TRANSACTIONS,
    # ]
    # updates = api.get_update(option_list=option_list, session_id=session_id)
    # print(updates)