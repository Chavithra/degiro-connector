import datetime

from google.protobuf import json_format
from google.protobuf.message import Message
from degiro_connector.trading.pb.trading_pb2 import (
    AccountOverview,
    Agenda,
    CashAccountReport,
    CompanyProfile,
    CompanyRatios,
    Favourites,
    FinancialStatements,
    LatestNews,
    NewsByCompany,
    Order,
    OrdersHistory,
    ProductsInfo,
    ProductSearch,
    TopNewsPreview,
    TransactionsHistory,
    Update,
)
from typing import Dict, List, Union

# MATCHINGS
__ACTION_MATCHING = {
    'B': Order.Action.Value('BUY'),
    'S': Order.Action.Value('SELL'),
}

__ORDER_MATCHING = {
    'buysell': 'action',
    'contractSize': 'contract_size',
    'contractType': 'contract_type',
    'currency': 'currency',
    'date': 'hour',
    'id': 'id',
    'isDeletable': 'is_deletable',
    'isModifiable': 'is_modifiable',
    'orderTimeTypeId': 'time_type',
    'orderTypeId': 'order_type',
    'price': 'price',
    'product': 'product',
    'productId': 'product_id',
    'quantity': 'quantity',
    'size': 'size',
    'stopPrice': 'stop_price',
    'totalOrderValue': 'total_order_value',
}

__UPDATE_OPTION_MATCHING = {
    Update.Option.Value('ALERTS'): 'alerts',
    Update.Option.Value('CASHFUNDS'): 'cashFunds',
    Update.Option.Value('HISTORICALORDERS'): 'historicalOrders',
    Update.Option.Value('ORDERS'): 'orders',
    Update.Option.Value('PORTFOLIO'): 'portfolio',
    Update.Option.Value('TOTALPORTFOLIO'): 'totalPortfolio',
    Update.Option.Value('TRANSACTIONS'): 'transactions',
}


# GRPC TO API
def account_overview_request_to_api(
    request: AccountOverview.Request,
) -> dict:
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


def cash_account_report_request_to_api(
    request: CashAccountReport.Request,
) -> dict:
    request_dict = dict()
    request_dict['country'] = request.country
    request_dict['lang'] = request.lang
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


def agenda_request_to_api(
    request: Agenda.Request,
) -> dict:
    request_dict = json_format.MessageToDict(
        message=request,
        including_default_value_fields=False,
        preserving_proto_field_name=False,
        use_integers_for_enums=True,
        descriptor_pool=None,
        float_precision=None,
    )
    request_dict['calendarType'] = Agenda \
        .CalendarType \
        .Name(request.calendar_type) \
        .title() \
        .replace('_', '')
    request_dict['offset'] = request.offset
    request_dict['orderByDesc'] = request.order_by_desc

    return request_dict


def latest_news_request_to_api(
    request: LatestNews.Request,
) -> dict:
    request_dict = {
        'offset': request.offset,
        'languages': request.languages,
        'limit': request.limit,
    }

    return request_dict


def news_by_company_request_to_api(
    request: NewsByCompany.Request,
) -> dict:
    request_dict = {
        'isin': request.isin,
        'limit': request.limit,
        'offset': request.offset,
        'languages': request.languages,
    }

    return request_dict


def order_to_api(order: Order) -> Dict[str, Union[float, int, str]]:
    # Build dict from message
    order_dict = json_format.MessageToDict(
        message=order,
        including_default_value_fields=True,
        preserving_proto_field_name=False,
        use_integers_for_enums=True,
        descriptor_pool=None,
        float_precision=None,
    )

    # Setup 'buySell'
    if order.action == order.Action.BUY:
        order_dict['buySell'] = 'BUY'
    else:
        order_dict['buySell'] = 'SELL'

    # Filter fields
    fields_to_keep = {
        'buySell',
        'orderType',
        'price',
        'stopPrice',
        'productId',
        'size',
        'timeType',
    }
    filtered_order_dict = dict()
    for field in order_dict.keys() & fields_to_keep:
        filtered_order_dict[field] = order_dict[field]

    return filtered_order_dict


def orders_history_request_to_api(request: OrdersHistory.Request) -> dict:
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


def products_info_to_api(
    request: ProductsInfo.Request,
) -> List[str]:
    request_dict = json_format.MessageToDict(
        message=request,
        including_default_value_fields=True,
        preserving_proto_field_name=False,
        use_integers_for_enums=True,
        descriptor_pool=None,
        float_precision=None,
    )
    payload = request_dict['products']
    payload = list(map(str, payload))

    return payload


def product_search_request_to_api(
    request: Union[
        ProductSearch.RequestBonds,
        ProductSearch.RequestETFs,
        ProductSearch.RequestFunds,
        ProductSearch.RequestFutures,
        ProductSearch.RequestLeverageds,
        ProductSearch.RequestLookup,
        ProductSearch.RequestOptions,
        ProductSearch.RequestStocks,
        ProductSearch.RequestWarrants,
    ],
) -> dict:
    request_dict = json_format.MessageToDict(
        message=request,
        including_default_value_fields=False,
        preserving_proto_field_name=False,
        use_integers_for_enums=True,
        descriptor_pool=None,
        float_precision=None,
    )

    return request_dict


def transactions_history_request_to_api(
    request: TransactionsHistory.Request,
) -> dict:
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


def update_request_list_to_api(request_list: Update.RequestList) -> dict:
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


# API TO GRPC
def account_overview_to_grpc(payload: dict) -> AccountOverview:
    account_overview = AccountOverview()
    account_overview.response_datetime.GetCurrentTime()
    json_format.ParseDict(
        js_dict={'values': payload['data']},
        message=account_overview,
        ignore_unknown_fields=True,
        descriptor_pool=None,
    )

    return account_overview


def cash_account_report_to_grpc(
    request: CashAccountReport.Request,
    payload: str,
) -> CashAccountReport:
    cash_account_report = CashAccountReport()
    cash_account_report.response_datetime.GetCurrentTime()
    cash_account_report.content = payload
    cash_account_report.format = request.format

    return cash_account_report


def agenda_to_grpc(
    request: Agenda.Request,
    payload: dict,
) -> CashAccountReport:
    agenda = Agenda()
    agenda.response_datetime.GetCurrentTime()
    agenda.calendar_type = request.calendar_type
    json_format.ParseDict(
        js_dict=payload,
        message=agenda,
        ignore_unknown_fields=True,
        descriptor_pool=None,
    )

    return agenda



def checking_response_to_grpc(payload: dict) -> Order.CheckingResponse:
    checking_response = Order.CheckingResponse()
    checking_response.response_datetime.GetCurrentTime()
    json_format.ParseDict(
        js_dict=payload['data'],
        message=checking_response,
        ignore_unknown_fields=True,
        descriptor_pool=None,
    )

    return checking_response


def company_profile_to_grpc(payload: dict) -> CompanyProfile:
    company_profile = CompanyProfile()
    json_format.ParseDict(
        js_dict={'values': payload['data']},
        message=company_profile,
        ignore_unknown_fields=False,
        descriptor_pool=None,
    )
    return company_profile


def company_ratios_to_grpc(payload: dict) -> CompanyRatios:
    company_ratios = CompanyRatios()
    json_format.ParseDict(
        js_dict={'values': payload['data']},
        message=company_ratios,
        ignore_unknown_fields=False,
        descriptor_pool=None,
    )
    return company_ratios


def confirmation_response_to_grpc(
    payload: dict,
) -> Order.ConfirmationResponse:
    confirmation_response = Order.ConfirmationResponse()
    confirmation_response.response_datetime.GetCurrentTime()
    json_format.ParseDict(
        js_dict=payload['data'],
        message=confirmation_response,
        ignore_unknown_fields=False,
        descriptor_pool=None,
    )

    return confirmation_response


def favourites_to_grpc(payload: dict) -> Favourites:
    favourites = Favourites()
    favourites.response_datetime.GetCurrentTime()
    json_format.ParseDict(
        js_dict={'values': payload['data']},
        message=favourites,
        ignore_unknown_fields=False,
        descriptor_pool=None,
    )

    return favourites


def financial_statements_to_grpc(payload: dict) -> CompanyProfile:
    financial_statements = FinancialStatements()
    json_format.ParseDict(
        js_dict={'values': payload['data']},
        message=financial_statements,
        ignore_unknown_fields=False,
        descriptor_pool=None,
    )
    return financial_statements


def latest_news_to_grpc(payload: dict) -> LatestNews:
    latest_news = LatestNews()
    json_format.ParseDict(
        js_dict=payload['data'],
        message=latest_news,
        ignore_unknown_fields=False,
        descriptor_pool=None,
    )

    return latest_news


def message_to_dict(message: Message) -> dict:
    return json_format.MessageToDict(
        message=message,
        including_default_value_fields=True,
        preserving_proto_field_name=True,
        use_integers_for_enums=True,
        descriptor_pool=None,
        float_precision=None,
    )


def news_by_company_to_grpc(payload: dict) -> NewsByCompany:
    news_by_company = NewsByCompany()
    json_format.ParseDict(
        js_dict=payload['data'],
        message=news_by_company,
        ignore_unknown_fields=False,
        descriptor_pool=None,
    )

    return news_by_company


def orders_history_to_grpc(payload: dict) -> OrdersHistory:
    orders_history = OrdersHistory()
    orders_history.response_datetime.GetCurrentTime()
    json_format.ParseDict(
        js_dict={'values': payload['data']},
        message=orders_history,
        ignore_unknown_fields=True,
        descriptor_pool=None,
    )

    return orders_history


def products_config_to_grpc(payload: dict) -> ProductSearch.Config:
    products_config = ProductSearch.Config()
    json_format.ParseDict(
        js_dict={'values': payload},
        message=products_config,
        ignore_unknown_fields=False,
        descriptor_pool=None,
    )

    return products_config


def products_info_to_grpc(payload: dict) -> ProductsInfo:
    products_info = ProductsInfo()
    json_format.ParseDict(
        js_dict={'values': payload['data']},
        message=products_info,
        ignore_unknown_fields=False,
        descriptor_pool=None,
    )
    return products_info


def product_search_to_grpc(payload: dict) -> ProductSearch:
    product_search = ProductSearch()
    product_search.response_datetime.GetCurrentTime()
    json_format.ParseDict(
        js_dict=payload,
        message=product_search,
        ignore_unknown_fields=True,
        descriptor_pool=None,
    )

    return product_search


def setup_update_orders(update: Update, payload: dict):
    """ Build an "Order" object using "dict" returned by the API.
    Parameters:
        order {dict}
            Order dict straight from Degiro's API
    Returns:
        {Order}
    """

    if 'orders' in payload:
        update.orders.last_updated = \
            payload['orders']['lastUpdated']

        for order in payload['orders']['value']:
            order_dict = dict()
            for attribute in order['value']:
                if 'name' in attribute \
                        and 'value' in attribute \
                        and attribute['name'] in __ORDER_MATCHING:
                    order_dict[__ORDER_MATCHING[attribute['name']]] = \
                        attribute['value']

            order_dict['action'] = \
                __ACTION_MATCHING[order_dict['action']]
            update.orders.values.append(Order(**order_dict))


def setup_update_portfolio(update: Update, payload: dict):
    if 'portfolio' in payload:
        update.portfolio.last_updated = \
            payload['portfolio']['lastUpdated']

        for positionrow in payload['portfolio']['value']:
            value = update.portfolio.values.add()
            for attribute in positionrow['value']:
                if 'name' in attribute \
                        and 'value' in attribute:
                    value[attribute['name']] = attribute['value']


def setup_update_total_portfolio(update: Update, payload: dict):
    if 'totalPortfolio' in payload:
        update.total_portfolio.last_updated = \
            payload['totalPortfolio']['lastUpdated']

        for attribute in payload['totalPortfolio']['value']:
            if 'name' in attribute \
                    and 'value' in attribute:
                name = attribute['name']
                value = attribute['value']
                update.total_portfolio.values[name] = value


def top_news_preview_to_grpc(payload: dict) -> TopNewsPreview:
    top_news_preview = TopNewsPreview()
    json_format.ParseDict(
        js_dict=payload['data'],
        message=top_news_preview,
        ignore_unknown_fields=False,
        descriptor_pool=None,
    )

    return top_news_preview


def transactions_history_to_grpc(payload: dict) -> TransactionsHistory:
    transactions_history = TransactionsHistory()
    transactions_history.response_datetime.GetCurrentTime()
    json_format.ParseDict(
        js_dict={'values': payload['data']},
        message=transactions_history,
        ignore_unknown_fields=True,
        descriptor_pool=None,
    )

    return transactions_history


def update_to_grpc(payload: dict) -> Update:
    update = Update()
    update.response_datetime.GetCurrentTime()

    # ORDERS
    setup_update_orders(update=update, payload=payload)

    # PORTFOLIO
    setup_update_portfolio(
        update=update,
        payload=payload,
    )

    # TOTALPORTFOLIO
    setup_update_total_portfolio(
        update=update,
        payload=payload,
    )

    return update
