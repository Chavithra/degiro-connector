import logging
import quotecast.helpers.pb_handler as pb_handler
import requests
import time
import urllib3

from quotecast.constants.endpoint import Endpoint
from quotecast.constants.headers import Headers
from quotecast.pb.quotecast_pb2 import (
    Metadata,
    Quotecast,
    Request,
)
from typing import Union


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# pylint: disable=no-member

def build_logger()->logging.Logger:
    return logging.getLogger(__name__)

def build_session(headers:dict=None)->requests.Session:
    """ Setup a requests.Session object.

    Args:
        headers (dict, optional):
            Headers to used for the Session.
            Defaults to None.

    Returns:
        requests.Session:
            Session object with the right headers.
    """

    session = requests.Session()

    if isinstance(headers, dict) :
        session.headers.update(headers)
    else:
        session.headers.update(Headers.get_headers())

    return session

def get_session_id(
    user_token:int,
    session:requests.Session=None,
    logger:logging.Logger=None,
)->str:
    """ Retrieve the "session_id" necessary to access the data-stream.

    Args:
        user_token (int):
            User identifier in Degiro's API.
        session (requests.Session, optional):
            This object will be generated if None.
            Defaults to None.
        logger (logging.Logger, optional):
            This object will be generated if None.
            Defaults to None.

    Returns:
        str: Session id
    """

    if logger is None:
        logger = build_logger()
    if session is None:
        session = build_session()
    
    url = Endpoint.URL
    url = f'{url}/request_session'
    version = Endpoint.VERSION
    
    parameters = {'version': version, 'userToken': user_token}
    data = '{"referrer":"https://trader.degiro.nl"}'

    request = requests.Request(
        method='POST',
        url=url,
        data=data,
        params=parameters
    )
    prepped = session.prepare_request(request=request)

    try:
        response = session.send(request=prepped, verify=False)
        response_dict = response.json()
    except Exception as e:
        logger.fatal(e)
        return False
    
    logger.info('get_session_id:response_dict: %s', response_dict)

    if 'sessionId' in response_dict:
        return response_dict['sessionId']
    else:
        return None

def fetch_data(
    session_id:str,
    session:requests.Session=None,
    logger:logging.Logger=None,
)->Quotecast:
    """ Fetch data from the feed.

    Args:
        session_id (str):
            API's session id.
        session (requests.Session, optional):
            This object will be generated if None.
            Defaults to None.
        logger (logging.Logger, optional):
            This object will be generated if None.
            Defaults to None.

    Raises:
        BrokenPipeError:
            A new "session_id" is required.

    Returns:
        Quotecast:
            quotecast.json_data : raw JSON data string.
            quotecast.metadata.response_datetime : reception timestamp.
            quotecast.metadata.request_duration : request duration.
    """

    if logger is None:
        logger = build_logger()
    if session is None:
        session = build_session()

    url = f'{Endpoint.URL}/{session_id}'

    request = requests.Request(method='GET', url=url)
    prepped = session.prepare_request(request=request)

    start_ns = time.perf_counter_ns()
    response = session.send(request=prepped, verify=False)
    # We could have used : response.elapsed.total_seconds()
    duration_ns = time.perf_counter_ns() - start_ns

    if response.text == '[{"m":"sr"}]' :
        raise BrokenPipeError('A new "session_id" is required.')

    quotecast = Quotecast()
    quotecast.json_data = response.text
    # There is no "date" header returned
    # We could have used : response.cookies._now
    quotecast.metadata.response_datetime.GetCurrentTime()
    quotecast.metadata.request_duration.FromNanoseconds(duration_ns)

    return quotecast

def subscribe(
    request:Request,
    session_id:str,
    session:requests.Session=None,
    logger:logging.Logger=None,
)->bool:
    """ Add/remove metric from the data-stream.

    Args:
        request (Request):
            List of subscriptions & unsubscriptions to do.
            Example :
            request = Request()
            request.subscriptions['360015751'].extend([
                'LastPrice',
                'LastVolume',
            ])
            request.subscriptions['AAPL.BATS,E'].extend([
                'LastPrice',
                'LastVolume',
            ])
            request.unsubscriptions['360015751'].extend([
                'LastPrice',
                'LastVolume',
            ])
        session_id (str):
            API's session id.
        session (requests.Session, optional):
            This object will be generated if None.
            Defaults to None.
        logger (logging.Logger, optional):
            This object will be generated if None.
            Defaults to None.

    Raises:
        BrokenPipeError:
            A new "session_id" is required.

    Returns:
        bool:
            Whether or not the subscription succeeded.
    """

    if logger is None:
        logger = build_logger()
    if session is None:
        session = build_session()
    
    url = Endpoint.URL
    url = f'{url}/{session_id}'

    data = pb_handler.request_to_api(request=request)

    logger.info('subscribe:data %s', data[:100])

    session_request = requests.Request(method='POST', url=url, data=data)
    prepped = session.prepare_request(request=session_request)
    
    try:
        response_raw = session.send(request=prepped, verify=False)
        request.status_code = response_raw.status_code

        if response_raw.text == '[{"m":"sr"}]' :
            raise BrokenPipeError('A new "session_id" is required.')
        else:
            response = True
    except Exception as e:
        logger.fatal(e)
        return False

    return response