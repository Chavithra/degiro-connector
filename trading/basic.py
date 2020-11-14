import logging
import trading.utilities as utilities

from typing import (
    List,
    Union,
)
from quotecast.constants.headers import Headers
from trading.models.session_storage import SessionStorage
from trading.pb.trading_pb2 import (
    Credentials,
    Order,
    OrdersHistory,
    Update,
)

class Basic:
    """ Wrapper for "degiro.trading.api.utilities" module.
    
    Improvements compared to "utilities" module :
    1/ Credentials
        No need to re-enter the credentials for each function.
    2/ Sessions
        The "requests.Session" object is reuse in a thread safe manner.
    3/ Logging
    """

    @property
    def credentials(self)->Credentials:
        return self._credentials

    @property
    def session_storage(self)->SessionStorage:
        return self._session_storage

    @session_storage.setter
    def session_storage(self, session_storage:SessionStorage):
        self._session_storage = session_storage

    def build_session_storage(self)->SessionStorage:
        return SessionStorage(
            headers=Headers.get_headers(),
            hooks=None
        )

    def __init__(
        self,
        credentials:Credentials,
        session_storage=None,
    ):
        if session_storage is None:
            session_storage = self.build_session_storage()

        self._logger = logging.getLogger(self.__module__)
        self._credentials = credentials
        self._session_storage = session_storage
    
    def get_session_id(self)->str:
        credentials = self._credentials
        logger = self._logger
        session = self._session_storage.session

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
        credentials = self._credentials
        logger = self._logger
        session = self._session_storage.session

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
        credentials = self._credentials
        logger = self._logger
        session = self._session_storage.session

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
        credentials = self._credentials
        logger = self._logger
        session = self._session_storage.session

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
        credentials = self._credentials
        logger = self._logger
        session = self._session_storage.session

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
        credentials = self._credentials
        logger = self._logger
        session = self._session_storage.session

        return utilities.delete_order(
            order_id=order_id,
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )

    def get_config(
        self,
        session_id:str,
    )->dict:
        credentials = self._credentials
        logger = self._logger
        session = self._session_storage.session

        return utilities.get_config(
            session_id=session_id,
            session=session,
            logger=logger,
        )

    def get_client_details(
        self,
        session_id:str,
        raw:bool=False,
    )->dict:
        credentials = self._credentials
        logger = self._logger
        session = self._session_storage.session

        return utilities.get_client_details(
            session_id=session_id,
            raw=raw,
            session=session,
            logger=logger,
        )

    def get_client_info(
        self,
        session_id:str,
        raw:bool=False,
    )->dict:
        credentials = self._credentials
        logger = self._logger
        session = self._session_storage.session

        return utilities.get_client_info(
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )

    def get_order_history(
        self,
        request:OrdersHistory.Request,
        session_id:str,
        raw:bool=False,
    )->Union[dict, Update]:
        credentials = self._credentials
        logger = self._logger
        session = self._session_storage.session

        return utilities.get_order_history(
            request=request,
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )

    def get_transactions_history(
        self,
        request:OrdersHistory.Request,
        session_id:str,
        raw:bool=False,
    )->Union[dict, Update]:
        credentials = self._credentials
        logger = self._logger
        session = self._session_storage.session

        return utilities.get_transactions_history(
            request=request,
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )

    def get_account_overview(
        self,
        request:OrdersHistory.Request,
        session_id:str,
        raw:bool=False,
    )->Union[dict, Update]:
        credentials = self._credentials
        logger = self._logger
        session = self._session_storage.session

        return utilities.get_account_overview(
            request=request,
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )

    def products_lookup(
        self,
        request:OrdersHistory.Request,
        session_id:str,
        raw:bool=False,
    )->Union[dict, Update]:
        credentials = self._credentials
        logger = self._logger
        session = self._session_storage.session

        return utilities.products_lookup(
            request=request,
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )

if __name__ == '__main__':
    import json

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