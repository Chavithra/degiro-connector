import datetime
from google.protobuf import json_format
from trading.pb.trading_pb2 import (
    AccountOverview,
    Order,
    OrdersHistory,
    Transaction,
    TransactionsHistory,
    Update,
)
from typing import (
    List,
    Union,
)

# MATCHINGS
__ACTION_MATCHING = {
    'B' : Order.Action.Value('BUY'),
    'S' : Order.Action.Value('SELL'),
}

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

__UPDATE_OPTION_MATCHING = {
    Update.Option.Value('ALERTS') : 'alerts',
    Update.Option.Value('CASHFUNDS') : 'cashFunds',
    Update.Option.Value('HISTORICALORDERS') : 'historicalOrders',
    Update.Option.Value('ORDERS') : 'orders',
    Update.Option.Value('PORTFOLIO') : 'portfolio',
    Update.Option.Value('TOTALPORTFOLIO') : 'totalPortfolio',
    Update.Option.Value('TRANSACTIONS') : 'transactions',
}

# GRPC TO API
def update_request_list_to_api(
    request_list:Update.RequestList,
)->dict:
    """ Makes a payload compatible with the API.

    Parameters:
        update_option_list {UpdateOptionList}
            List of option available from grpc "consume_update".

    Returns:
        {dict}
            Payload that Degiro's update endpoint can understand.
    """

    payload = dict()

    for request in request_list.values:
        option = __UPDATE_OPTION_MATCHING[request.option]
        payload[option] = request.last_update

    return payload

def orders_history_request_to_api(
    request:OrdersHistory.Request,
)->dict:
    request_dict = json_format.MessageToDict(
        message=request,
        including_default_value_fields=True,
        preserving_proto_field_name=False,
    )

    return request_dict

def transactions_request_to_api(
    request:OrdersHistory.Request,
)->dict:
    request_dict = json_format.MessageToDict(
        message=request,
        including_default_value_fields=True,
        preserving_proto_field_name=False,
    )

    return request_dict


def account_overview_request_to_api(
    request:OrdersHistory.Request,
)->dict:
    request_dict = json_format.MessageToDict(
        message=request,
        including_default_value_fields=True,
        preserving_proto_field_name=False,
    )

    return request_dict

# API TO GRPC
def order_to_grpc(
    order_dict:dict,
    return_dict:bool=False,
)->Union[Order, dict]:
    """ Build an "Order" object using "dict" returned by the API.
    Parameters:
        order {dict}
            Order dict straight from Degiro's API
    Returns:
        {Order}
    """

    order_attribute_dict = dict()
    for attribute in order_dict['value']:
        if \
            'name' in attribute \
            and 'value' in attribute:
            name = attribute['name']
            value = attribute['value']
            order_attribute_dict[name] = value

    order_dict = dict()
    for field in __ORDER_MATCHING:
        if field in order_attribute_dict:
            order_dict[__ORDER_MATCHING[field]] = order_attribute_dict[field]

    order_dict['action'] = __ACTION_MATCHING[order_dict['action']]

    if return_dict == True:
        return order_dict
    else:
        return Order(**order_dict)

def update_to_grpc(
    update_dict:dict
)->Update:

    update = Update()
    
    # TOTALPORTFOLIO
    if 'totalPortfolio' in update_dict:

        total_portfolio_dict_values = dict()
        for attribute in update_dict['totalPortfolio']['value']:
            if \
                'name' in attribute \
                and 'value' in attribute:
                name = attribute['name']
                value = attribute['value']
                total_portfolio_dict_values[name] = value


        total_portfolio_dict = dict()
        total_portfolio_dict['last_update'] = update_dict['totalPortfolio']['lastUpdated']
        total_portfolio_dict['values'] = total_portfolio_dict_values

        json_format.ParseDict(
            js_dict=total_portfolio_dict,
            message=update.total_portfolio,
            ignore_unknown_fields=True,
        )

    # PORTFOLIO
    if 'portfolio' in update_dict:

        position_row_list = list()
        for positionrow in update_dict['portfolio']['value']:
            positionrow_dict = dict()
            for attribute in positionrow['value']:
                if \
                    'name' in attribute \
                    and 'value' in attribute:
                    name = attribute['name']
                    value = attribute['value']
                    positionrow_dict[name] = value
            position_row_list.append(positionrow_dict)

        portfolio_dict = dict()
        portfolio_dict['last_update'] = update_dict['portfolio']['lastUpdated']
        portfolio_dict['position_row_list'] = position_row_list

        json_format.ParseDict(
            js_dict=portfolio_dict,
            message=update.portfolio,
            ignore_unknown_fields=True,
        )

    # ORDERS
    if 'orders' in update_dict:

        order_list = list()
        for order in update_dict['orders']['value']:
            order_dict = order_to_grpc(
                order_dict=order,
                return_dict=True,
            )
            order_list.append(order_dict)

        orders_dict = dict()
        orders_dict['last_update'] = update_dict['orders']['lastUpdated']
        orders_dict['order_list'] = order_list

        json_format.ParseDict(
            js_dict=orders_dict,
            message=update.orders,
            ignore_unknown_fields=True,
        )
    
    return update

def checking_response_to_grpc(
    checking_dict:dict,
)->Order.CheckingResponse:
    js_dict = checking_dict['data']
    js_dict['response_datetime'] = str(datetime.datetime.now())
    checking_response = Order.CheckingResponse()
    json_format.ParseDict(
        js_dict=js_dict,
        message=checking_response,
    )

    return checking_response

def confirmation_response_to_grpc(
    confirmation_dict:dict,
)->Order.ConfirmationResponse:
    js_dict = confirmation_dict['data']
    js_dict['response_datetime'] = str(datetime.datetime.now())
    confirmation_response = Order.ConfirmationResponse()
    json_format.ParseDict(
        js_dict=js_dict,
        message=confirmation_response,
    )

    return confirmation_response

def orders_history_to_grpc(
    orders_history_dict:dict,
)->OrdersHistory:
    js_dict = orders_history_dict['data']
    js_dict['response_datetime'] = str(datetime.datetime.now())
    orders_history = OrdersHistory()
    json_format.ParseDict(
        js_dict=js_dict,
        message=orders_history,
    )

    return orders_history

def transactions_history_to_grpc(
    transactions_history_dict:dict,
)->TransactionsHistory:
    js_dict = transactions_history_dict['data']
    js_dict['response_datetime'] = str(datetime.datetime.now())
    transactions_history = TransactionsHistory()
    json_format.ParseDict(
        js_dict=js_dict,
        message=transactions_history,
    )

    return transactions_history

def account_overview_to_grpc(
    account_overview_dict:dict,
)->OrdersHistory:
    js_dict = account_overview_dict['data']
    js_dict['response_datetime'] = str(datetime.datetime.now())
    account_overview = AccountOverview()
    json_format.ParseDict(
        js_dict=js_dict,
        message=account_overview,
    )

    return account_overview