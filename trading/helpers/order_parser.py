from trading.pb.broker_pb2 import (
    Order,
    Action,
    UpdateOption,
    UpdateOptionList,
)

class OrderParser:
    __ORDER_MATCHING = {
        'buysell' : 'action',
        'contractSize' : 'contract_size',
        'contractType' : 'contract_type',
        'currency' : 'currency',
        'date' : 'hour',
        'id' : 'id',
        'isDeletable' : 'is_deletable',
        'isModifiable' : 'is_modifiable',
        'orderTimeTypeId' : 'time_type',
        'orderTypeId' : 'order_type',
        'price' : 'price',
        'product' : 'product',
        'productId' : 'product_id',
        'quantity' : 'quantity',
        'size' : 'size',
        'stopPrice' : 'stop_price',
        'totalOrderValue' : 'total_order_value',
    }

    __ACTION_MATCHING = {
        'B' : Action.Value('BUY'),
        'S' : Action.Value('SELL'),
    }

    @classmethod
    def api_to_grpc_order(cls, order:dict)->Order:
        """ Build an "Order" object using "dict" returned by the API.

        Parameters:
            order {dict}
                Order dict straight from Degiro's API

        Returns:
            {Order}
        """

        order = order['value']
        order = {element['name']:element['value'] for element in order}

        order_new = dict()
        for field in cls.__ORDER_MATCHING:
            if field in order:
                order_new[cls.__ORDER_MATCHING[field]] = order[field]

        order_new['action'] = cls.__ACTION_MATCHING[order_new['action']]

        return Order(**order_new)