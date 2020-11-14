import logging

from trading.basic import Basic
from trading.models.connection_storage import ConnectionStorage
from trading.pb.trading_pb2 import (
    Credentials,
    Order,
    OrdersHistory,
    Update,
)
from typing import (
    List,
    Union,
)
from wrapt.decorators import synchronized
    
class API:
    """ Same operation then Basic but with "session_id" management. """

    @property
    def basic(self)->Basic:
        """ Getter for the attribute : self._basic
        
        Returns:
            {Basic} -- Current Basic object.
        """

        return self._basic

    @basic.setter
    def basic(self, basic:Basic):
        """ Setter for the attribute : self._basic

        Arguments:
            basic {Basic} -- New Basic object.
        """

        self._basic = basic
    
    
    @property
    def connection_storage(self)->Basic:
        """ Getter for the attribute : self._connection_storage
        
        Returns:
            {Basic} -- Current ConnectionStorage object.
        """

        return self._connection_storage

    @connection_storage.setter
    def connection_storage(
        self,
        connection_storage:ConnectionStorage,
    ):
        """ Setter for the attribute : self._connection_storage

        Arguments:
            connection_storage {ConnectionStorage} -- New ConnectionStorage object.
        """

        self._connection_storage = connection_storage

    def __init__(self, credentials:Credentials):
        self.logger = logging.getLogger(self.__module__)
        self._basic = Basic(credentials=credentials)
        self._connection_storage = ConnectionStorage(basic=self._basic)

    def get_update(
        self,
        request_list:Update.RequestList,
        raw:bool=False,
    ):
        basic = self._basic
        session_id = self._connection_storage.session_id

        return basic.get_update(
            request_list=request_list,
            session_id=session_id,
            raw=raw,
        )

    def check_order(
        self, 
        order:Order,
        raw:bool=False,
    )->Union[Order.ConfirmationResponse, bool]:
        basic = self._basic
        session_id = self._connection_storage.session_id

        return basic.check_order(
            order=order,
            session_id=session_id,
            raw=raw,
        )

    def confirm_order(
        self,
        confirmation_id:str,
        order:Order,
        raw:bool=False,
    )->Union[Order.ConfirmationResponse, bool]:
        basic = self._basic
        session_id = self._connection_storage.session_id

        return basic.confirm_order(
            confirmation_id=confirmation_id,
            order=order,
            session_id=session_id,
            raw=raw,
        )
    
    def update_order(
        self, 
        order:Order,
        raw:bool=False,
    ):
        basic = self._basic
        session_id = self._connection_storage.session_id

        return basic.update_order(
            order=order,
            session_id=session_id,
            raw=raw,
        )

    def delete_order(
        self,
        order_id:str
    )->bool:
        basic = self._basic
        session_id = self._connection_storage.session_id

        return basic.delete_order(
            order_id=order_id,
            session_id=session_id
        )

    def get_config(
        self,
    )->dict:
        basic = self._basic
        session_id = self._connection_storage.session_id

        return basic.get_config(
            session_id=session_id,
        )

    def get_client_details(
        self,
        raw:bool=False,
    )->dict:
        basic = self._basic
        session_id = self._connection_storage.session_id

        return basic.get_client_details(
            session_id=session_id,
            raw=raw,
        )

    def get_client_info(
        self,
        raw:bool=False,
    )->dict:
        basic = self._basic
        session_id = self._connection_storage.session_id

        return basic.get_client_info(
            session_id=session_id,
            raw=raw,
        )

    def get_order_history(
        self,
        request:OrdersHistory.Request,
        raw:bool=False,
    )->Union[dict, Update]:
        basic = self._basic
        session_id = self._connection_storage.session_id

        return basic.get_order_history(
            request=request,
            session_id=session_id,
            raw=raw,
        )

    def get_transactions_history(
        self,
        request:OrdersHistory.Request,
        raw:bool=False,
    )->Union[dict, Update]:
        basic = self._basic
        session_id = self._connection_storage.session_id

        return basic.get_transactions_history(
            request=request,
            session_id=session_id,
            raw=raw,
        )

    def get_account_overview(
        self,
        request:OrdersHistory.Request,
        raw:bool=False,
    )->Union[dict, Update]:
        basic = self._basic
        session_id = self._connection_storage.session_id

        return basic.get_account_overview(
            request=request,
            session_id=session_id,
            raw=raw,
        )

    def products_lookup(
        self,
        request:OrdersHistory.Request,
        raw:bool=False,
    )->Union[dict, Update]:
        basic = self._basic
        session_id = self._connection_storage.session_id

        return basic.products_lookup(
            request=request,
            session_id=session_id,
            raw=raw,
        )

if __name__ == "__main__":
    import json

    from trading.pb.trading_pb2 import (
        Order,
        Update,
    )
    with open('config/config.json') as config_file:
        config = json.load(config_file)

    int_account = config['int_account']
    username = config['username']
    password = config['password']
    credentials = Credentials(
        int_account=int_account,
        username=username,
        password=password
    )
    api = API(credentials=credentials)

    # INITIALIZATION

    api.connection_storage.connect()

    print(api.connection_storage.session_id)
    
    # order = Order(
    #     action=Order.Action.BUY,
    #     order_type=Order.OrderType.LIMIT,
    #     price=10.60,
    #     product_id=71981,
    #     size=1,
    #     time_type=Order.TimeType.GOOD_TILL_DAY,
    # )
    # print(order)
    # confirmation_id = api.check_order(order=order)
    # order = api.confirm_order(
    #     confirmation_id=confirmation_id,
    #     order=order
    # )

    # print('session_id', api.connection_storage.session_id)
    # print('confirmation_id', confirmation_id)
    # print('order', order)