from trading.pb.broker_pb2 import (
    Order,
    Action,
    Update,
    UpdateOption,
    UpdateOptionList,
)

from trading.helpers.order_parser import OrderParser
from trading.helpers.transaction_parser import TransactionParser

class UpdateParser:
    __UPDATE_OPTION_MATCHING = {
        UpdateOption.Value('ALERTS') : 'alerts',
        UpdateOption.Value('CASHFUNDS') : 'cashFunds',
        UpdateOption.Value('HISTORICALORDERS') : 'historicalOrders',
        UpdateOption.Value('ORDERS') : 'orders',
        UpdateOption.Value('PORTFOLIO') : 'portfolio',
        UpdateOption.Value('TOTALPORTFOLIO') : 'totalPortfolio',
        UpdateOption.Value('TRANSACTIONS') : 'transactions',
    }
    
    @classmethod
    def grpc_to_api_update_option_list(
            cls,
            option_list:UpdateOptionList
        )->dict:
        """ Makes a payload compatible with the API.

        Paramters:
            option_list {UpdateOptionList}
                List of option available from grpc "consume_update".

        Returns:
            {dict}
                Payload that Degiro's update endpoint can understand.
        """

        api_payload = dict()
        for option in option_list.list:
            api_payload[cls.__UPDATE_OPTION_MATCHING[option]] = 0

        return api_payload
    
    @classmethod
    def api_to_grpc_update(
            cls,
            update:dict
        ):
        api_order_list = update['orders']['value']
        grpc_order_list = list()
        for api_order in api_order_list:
            grpc_order_list.append(
                OrderParser.api_to_grpc_order(order=api_order)
            )

        api_transaction_list = update['transactions']['value']
        grpc_transaction_list = list()
        for transaction in api_transaction_list:
            grpc_transaction_list.append(
                TransactionParser.api_to_grpc_transaction(
                    transaction=transaction
                )
            )

        update = Update(
            order_list=grpc_order_list,
            transaction_list=grpc_transaction_list
        )
        
        return update