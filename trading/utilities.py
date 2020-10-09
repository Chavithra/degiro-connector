import json
import logging
import requests
import urllib3

from trading.constants import URLs, Headers
from trading.pb.trading_pb2 import (
    Credentials,
    Order,
    Update,
    UpdateOptionList,
)
from trading.helpers.update_parser import UpdateParser
from trading.helpers.order_parser import OrderParser
from typing import List

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def build_logger():
    return logging.getLogger(__name__)

def build_session(headers:dict=None) -> requests.Session:
    """ Setup a requests.Session object.

    Arguments:
    headers {dict} -- Headers to used for the Session.

    Returns:
    {requests.Session} -- Session object with the right headers.
    """

    session = requests.Session()

    if isinstance(headers, dict) :
        session.headers.update(headers)
    else:
        session.headers.update(Headers.get_headers())

    return session

def get_session_id(
        credentials:Credentials,
        session:requests.Session=None,
        logger:logging.Logger=None
    )->str:
    """ Retrieve "session_id".
    This "session_id" is used by most Degiro's trading endpoint.
    Parameters:
        credentials {Credentials}
            credentials.username is necessary.
            credentials.password is necessary.
        session {requests.Session} (default: {None})
            If you one wants to reuse existing "Session" object.
        logger {logging.Logger} (default: {None})
            If you one wants to reuse existing "Logger" object.
    Raises:
        {ConnectionError}: It means the connection failed.
    Returns:
        {str} -- Session id
    """

    if logger is None:
        logger = build_logger()
    if session is None:
        session = build_session()
    
    url = URLs.LOGIN
    username = credentials.username
    password = credentials.password

    payload_dict = {
        'username': username,
        'password': password,
        'isPassCodeReset': False,
        'isRedirectToMobile': False,
        'queryParams': {}
    }

    request = requests.Request(method='POST', url=url, json=payload_dict)
    prepped = session.prepare_request(request)

    try:
        response = session.send(prepped, verify=False)
        response_dict = response.json()
    except Exception as e:
        raise ConnectionError(e)
    
    logger.info('get_session_id:response_dict: %s', response_dict)

    if 'sessionId' in response_dict:
        return response_dict['sessionId']
    else:
        raise ConnectionError('No session id returned.')
  
def get_update(
        option_list:UpdateOptionList,
        session_id:str,
        credentials:Credentials,
        session:requests.Session=None,
        logger:logging.Logger=None
    )->Update:
    """ Retrieve information from Degiro's Trading Update endpoint.

    Parameters:
        session_id {str}
            Degiro's session id
        credentials {Credentials}
            Credentials containing the parameter "int_account".
        option_list {UpdateOptionList}
            List of options that we want to retrieve from the endpoint.
            Example :
                option_list = UpdateOptionList(
                    list = [
                        UpdateOption.ALERTS,
                        UpdateOption.CASHFUNDS,
                        UpdateOption.HISTORICALORDERS,
                        UpdateOption.ORDERS,
                        UpdateOption.PORTFOLIO,
                        UpdateOption.TOTALPORTFOLIO,
                        UpdateOption.TRANSACTIONS,
                    ]
                )
        session {requests.Session}
            This object will be generated if None. (default: {None})
        logger {logging.Logger}
            This object will be generated if None. (default: {None})

    Returns:
        Update -- API response.
    """
    
    if logger is None:
        logger = build_logger()
    if session is None:
        session = build_session()

    int_account = credentials.int_account
    url = URLs.UPDATE
    url = f'{url}/{int_account};jsessionid={session_id}'
    
    params = UpdateParser.grpc_to_api_update_option_list(
        option_list=option_list
    )
    params['intAccount'] = int_account
    params['sessionId'] = session_id
    
    request = requests.Request(method='GET', url=url, params=params)
    prepped = session.prepare_request(request)

    try:
        response = session.send(prepped, verify=False)
        response = response.text
        response = UpdateParser.api_to_grpc_update(response)
    except Exception as e:
        logger.fatal(e)
        return False

    return response

def check_order(
        order:Order,
        session_id:str,
        credentials:Credentials,
        session:requests.Session=None,
        logger:logging.Logger=None
    )->str:
    
    if logger is None:
        logger = build_logger()
    if session is None:
        session = build_session()

    int_account = credentials.int_account
    url = URLs.ORDER_CHECK
    url = f'{url};jsessionid={session_id}?intAccount={int_account}&sessionId={session_id}'

    order_dict = {
        'buySell' : order.action,
        'orderType' : order.order_type,
        'price' : order.price,
        'productId' : order.product_id,
        'size' : order.size,
        'timeType' : order.time_type,
    }

    request = requests.Request(method='POST', url=url, json=order_dict)
    prepped = session.prepare_request(request)

    try:
        response = session.send(prepped, verify=False)
        response = response.json()
    except Exception as e:
        logger.fatal(e)
        return False

    if (
        type(response) != dict
        or 'data' not in response
        or 'confirmationId' not in response['data']
    ): return False

    return response['data']['confirmationId']

def update_order(
        order:Order,
        session_id:str,
        credentials:Credentials,
        session:requests.Session=None,
        logger:logging.Logger=None
    )->str:
    
    if logger is None:
        logger = build_logger()
    if session is None:
        session = build_session()

    int_account = credentials.int_account
    order_id = order.id
    url = URLs.ORDER_UPDATE
    url = f'{url}/{order_id};jsessionid={session_id}?intAccount={int_account}&sessionId={session_id}'

    order_dict = {
        'buySell' : order.action,
        'orderType' : order.order_type,
        'price' : order.price,
        'productId' : order.product_id,
        'size' : order.size,
        'timeType' : order.time_type,
    }

    request = requests.Request(method='PUT', url=url, json=order_dict)
    prepped = session.prepare_request(request)

    try:
        response = session.send(prepped, verify=False)
    except Exception as e:
        logger.fatal(e)
        return False

    return response.status_code == 200

def confirm_order(
        confirmation_id:str,
        order:Order,
        session_id:str,
        credentials:Credentials,
        session:requests.Session=None,
        logger:logging.Logger=None
    ) -> Order:
    
    if logger is None:
        logger = build_logger()
    if session is None:
        session = build_session()

    int_account = credentials.int_account
    url = URLs.ORDER_CONFIRM
    url = f'{url}/{confirmation_id};jsessionid={session_id}?intAccount={int_account}&sessionId={session_id}'
    
    order_dict = {
        'buySell' : order.action,
        'orderType' : order.order_type,
        'price' : order.price,
        'productId' : order.product_id,
        'size' : order.size,
        'timeType' : order.time_type,
    }

    request = requests.Request(method='POST', url=url, json=order_dict)
    prepped = session.prepare_request(request)

    try:
        response = session.send(prepped, verify=False)
        response = response.json()
    except Exception as e:
        logger.fatal(e)
        return False

    if (
        type(response) != dict
        or 'data' not in response
        or 'orderId' not in response['data']
    ): return False

    order.id = response['data']['orderId']

    return order

def delete_order(
        order_id:str,
        session_id:str,
        credentials:Credentials,
        session:requests.Session=None,
        logger:logging.Logger=None
    )->bool:

    if logger is None:
        logger = build_logger()
    if session is None:
        session = build_session()

    int_account = credentials.int_account
    url = URLs.ORDER_DELETE
    url = f'{url}/{order_id};jsessionid={session_id}?intAccount={int_account}&sessionId={session_id}'

    request = requests.Request(method='DELETE', url=url)
    prepped = session.prepare_request(request)

    try:
        response = session.send(prepped, verify=False)
        response = response.json()
    except Exception as e:
        logger.fatal(e)
        return False
    
    if response.status_code != 200: return False

    return True


def get_config(
        session_id:str,
        session:requests.Session=None,
        logger:logging.Logger=None
    )->dict:

    if logger is None:
        logger = build_logger()
    if session is None:
        session = build_session()
    
    url = URLs.CONFIG

    request = requests.Request(method='GET', url=url)
    prepped = session.prepare_request(request)
    prepped.headers['cookie'] = 'JSESSIONID=' + session_id

    try:
        response = session.send(prepped, verify=False)
        response = response.json()
    except Exception as e:
        logger.fatal(e)
        return False

    if (
        type(response) != dict
        or 'data' not in response
    ): return False

    return response['data']


def get_client_details(
        session_id:str,
        session:requests.Session=None,
        logger:logging.Logger=None
    )->dict:

    if logger is None:
        logger = build_logger()
    if session is None:
        session = build_session()
    
    url = URLs.CLIENT_DETAILS
    url = f'{url}?sessionId={session_id}'
    url = '' + session_id
    
    request = requests.Request(method='GET', url=url)
    prepped = session.prepare_request(request)
    response = session.send(prepped, verify=False)

    print('prepared:', prepped.headers)
    print('response:', response.text)

    if response.status_code != 200: return False
    
    response_payload = response.json()

    if (
        type(response_payload) != dict
        or 'data' not in response_payload
    ): return False

    return response_payload['data']

def get_client_info(
        session_id:str,
        credentials:Credentials,
        session:requests.Session=None,
        logger:logging.Logger=None
    )->dict:

    if logger is None:
        logger = build_logger()
    if session is None:
        session = build_session()

    int_account = credentials.int_account
    url = URLs.CLIENT_INFO
    url = f'{url}/{int_account};jsessionid={session_id}'
    
    request = requests.Request(method='GET', url=url)
    prepped = session.prepare_request(request)
    response = session.send(prepped, verify=False)
    
    if response.status_code != 200: return False

    return response.json()

if __name__ == "__main__":
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
    session_id = get_session_id(credentials=credentials)
    
    print(session_id)