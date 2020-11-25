import datetime
from google.protobuf import json_format
from trading.pb.trading_pb2 import (
    AccountOverview,
    Order,
    OrdersHistory,
    ProductsLookup,
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
def update_request_list_to_api(request_list:Update.RequestList)->dict:
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
        payload[option] = request.last_updated

    return payload

def orders_history_request_to_api(request:OrdersHistory.Request)->dict:
    request_dict = dict()
    request_dict['fromDate'] = \
        datetime.datetime(
            year=request.from_date.year,
            month=request.from_date.month,
            day=request.from_date.day
        ) \
        .strftime('%d/%m/%Y')
    request_dict['toDate'] = \
        datetime.datetime(
            year=request.to_date.year,
            month=request.to_date.month,
            day=request.to_date.day
        ) \
        .strftime('%d/%m/%Y')

    return request_dict

def account_overview_request_to_api(
    request:AccountOverview.Request,
)->dict:
    request_dict = dict()
    request_dict['fromDate'] = \
        datetime.datetime(
            year=request.from_date.year,
            month=request.from_date.month,
            day=request.from_date.day
        ) \
        .strftime('%d/%m/%Y')
    request_dict['toDate'] = \
        datetime.datetime(
            year=request.to_date.year,
            month=request.to_date.month,
            day=request.to_date.day
        ) \
        .strftime('%d/%m/%Y')

    return request_dict

def transactions_history_request_to_api(
    request:TransactionsHistory.Request,
)->dict:
    request_dict = dict()
    request_dict['fromDate'] = \
        datetime.datetime(
            year=request.from_date.year,
            month=request.from_date.month,
            day=request.from_date.day
        ) \
        .strftime('%d/%m/%Y')
    request_dict['toDate'] = \
        datetime.datetime(
            year=request.to_date.year,
            month=request.to_date.month,
            day=request.to_date.day
        ) \
        .strftime('%d/%m/%Y')

    return request_dict

# API TO GRPC
def setup_update_orders(
    update:Update,
    update_payload:dict,
):
    """ Build an "Order" object using "dict" returned by the API.
    Parameters:
        order {dict}
            Order dict straight from Degiro's API
    Returns:
        {Order}
    """

    if 'orders' in update_payload:
        update.orders.last_updated = \
            update_payload['orders']['lastUpdated']

        for order in update_payload['orders']['value']:
            order_dict = dict()
            for attribute in order['value']:
                if  'name' in attribute \
                and 'value' in attribute \
                and attribute['name'] in __ORDER_MATCHING:
                    order_dict[__ORDER_MATCHING[attribute['name']]] = \
                        attribute['value']

            order_dict['action'] = \
                __ACTION_MATCHING[order_dict['action']]
            update.orders.values.append(Order(**order_dict))

def setup_update_portfolio(
    update:Update,
    update_payload:dict,
):
    if 'portfolio' in update_payload:
        update.portfolio.last_updated = \
            update_payload['portfolio']['lastUpdated']
            
        for positionrow in update_payload['portfolio']['value']:
            value = update.portfolio.values.add()
            for attribute in positionrow['value']:
                if  'name' in attribute \
                and 'value' in attribute:
                    value[attribute['name']] = attribute['value']

def setup_update_total_portfolio(
    update:Update,
    update_payload:dict,
):
    if 'totalPortfolio' in update_payload:
        update.total_portfolio.last_updated = \
            update_payload['totalPortfolio']['lastUpdated']

        for attribute in update_payload['totalPortfolio']['value']:
            if  'name' in attribute \
            and 'value' in attribute:
                name = attribute['name']
                value = attribute['value']
                update.total_portfolio.values[name] = value

def build_update_from_payload(update_payload:dict)->Update:
    update = Update()
    update.response_datetime.GetCurrentTime()

    # ORDERS
    setup_update_orders(update=update, update_payload=update_payload)

    # PORTFOLIO
    setup_update_portfolio(
        update=update,
        update_payload=update_payload,
    )

    # TOTALPORTFOLIO
    setup_update_total_portfolio(
        update=update,
        update_payload=update_payload,
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
    payload:dict,
)->OrdersHistory:
    orders_history = OrdersHistory()
    orders_history.response_datetime.GetCurrentTime()
    json_format.ParseDict(
        js_dict={'values':payload['data']},
        message=orders_history,
        ignore_unknown_fields=True,
    )

    return orders_history

def transactions_history_to_grpc(
    payload:dict,
)->TransactionsHistory:
    transactions_history = TransactionsHistory()
    transactions_history.response_datetime.GetCurrentTime()
    json_format.ParseDict(
        js_dict={'values':payload['data']},
        message=transactions_history,
        ignore_unknown_fields=True,
    )

    return transactions_history

def account_overview_to_grpc(
    payload:dict,
)->OrdersHistory:
    account_overview = AccountOverview()
    account_overview.response_datetime.GetCurrentTime()
    json_format.ParseDict(
        js_dict={'values':payload['data']},
        message=account_overview,
        ignore_unknown_fields=True,
    )

    return account_overview

def products_loopkup_to_grpc(
    payload:dict,
)->OrdersHistory:
    products_lookup = ProductsLookup()
    products_lookup.response_datetime.GetCurrentTime()
    json_format.ParseDict(
        js_dict=payload,
        message=products_lookup,
        ignore_unknown_fields=True,
    )

    return products_lookup