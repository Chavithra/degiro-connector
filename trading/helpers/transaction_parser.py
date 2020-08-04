from trading.pb.broker_pb2 import (
    Order,
    Action,
    Transaction,
    Update,
    UpdateOption,
    UpdateOptionList,
)

class TransactionParser:
    __TRANSACTION_MATCHING = {
        'buysell' : 'action',
        'currency' : 'currency',
        'date' : 'hour',
        'id' : 'id',
        'price' : 'price',
        'product' : 'product',
        'product_id' : 'product_id',
        'quantity' : 'quantity',
    }

    __ACTION_MATCHING = {
        'B' : Action.Value('BUY'),
        'S' : Action.Value('SELL'),
    }

    @classmethod
    def api_to_grpc_transaction(
            cls,
            transaction:dict
        )->Transaction:
        
        transaction = transaction['value']
        transaction = {element['name']:element['value'] for element in transaction}

        transaction_new = dict()
        for field in cls.__TRANSACTION_MATCHING:
            if field in transaction:
                transaction_new[cls.__TRANSACTION_MATCHING[field]] = transaction[field]

        transaction_new['action'] = cls.__ACTION_MATCHING[transaction_new['action']]

        return Transaction(**transaction_new)