import logging
import orjson as json
import degiro_connector.quotecast.helpers.pb_handler as pb_handler
import degiro_connector.quotecast.constants.urls as urls
import requests
import time
import urllib3

from degiro_connector.quotecast.constants.headers import Headers
from degiro_connector.quotecast.pb.quotecast_pb2 import (
    Chart,
    Quotecast,
)
from typing import Dict

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# pylint: disable=no-member


def build_logger() -> logging.Logger:
    return logging.getLogger(__name__)


def build_session(headers: dict = None) -> requests.Session:
    """ Setups a requests.Session object.

    Args:
        headers (dict, optional):
            Headers to used for the Session.
            Defaults to None.

    Returns:
        requests.Session:
            Session object with the right headers.
    """

    session = requests.Session()

    if isinstance(headers, dict):
        session.headers.update(headers)
    else:
        session.headers.update(Headers.get_headers())

    return session


def get_session_id(
    user_token: int,
    session: requests.Session = None,
    logger: logging.Logger = None,
) -> str:
    """ Retrieves the "session_id" necessary to access the data-stream.

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

    url = urls.QUOTECAST
    url = f'{url}/request_session'
    version = urls.QUOTECAST_VERSION

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
        response_dict = json.loads(response.text)
    except Exception as e:
        logger.fatal(e)
        return False

    logger.info('get_session_id:response_dict: %s', response_dict)

    if 'sessionId' in response_dict:
        return response_dict['sessionId']
    else:
        return None


def fetch_data(
    session_id: str,
    session: requests.Session = None,
    logger: logging.Logger = None,
) -> Quotecast:
    """ Fetches data from the feed.

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
            json_data : raw JSON data string.
            metadata.response_datetime : reception timestamp.
            metadata.request_duration : request duration.
    """

    if logger is None:
        logger = build_logger()
    if session is None:
        session = build_session()

    url = f'{urls.QUOTECAST}/{session_id}'

    request = requests.Request(method='GET', url=url)
    prepped = session.prepare_request(request=request)

    start_ns = time.perf_counter_ns()
    response = session.send(request=prepped, verify=False)
    # We could have used : response.elapsed.total_seconds()
    duration_ns = time.perf_counter_ns() - start_ns

    if response.text == '[{"m":"sr"}]':
        raise BrokenPipeError('A new "session_id" is required.')

    quotecast = Quotecast()
    quotecast.json_data = response.text
    # There is no "date" header returned
    # We could have used : response.cookies._now
    quotecast.metadata.response_datetime.GetCurrentTime()
    quotecast.metadata.request_duration.FromNanoseconds(duration_ns)

    return quotecast


def subscribe(
    request: Quotecast.Request,
    session_id: str,
    session: requests.Session = None,
    logger: logging.Logger = None,
) -> bool:
    """ Adds/removes metric from the data-stream.

    Args:
        request (QuotecastAPI.Request):
            List of subscriptions & unsubscriptions to do.
            Example :
                request = Quotecast.Request()
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

    url = urls.QUOTECAST
    url = f'{url}/{session_id}'
    data = pb_handler.quotecast_request_to_api(request=request)

    logger.info('subscribe:data %s', data[:100])

    session_request = requests.Request(method='POST', url=url, data=data)
    prepped = session.prepare_request(request=session_request)

    try:
        response = session.send(request=prepped, verify=False)

        if response.text == '[{"m":"sr"}]':
            raise BrokenPipeError('A new "session_id" is required.')
        else:
            response = True
    except Exception as e:
        logger.fatal(e)
        return False

    return response


def get_chart(
    request: Chart.Request,
    user_token: int,
    override: Dict[str, str] = None,
    raw: bool = False,
    session: requests.Session = None,
    logger: logging.Logger = None,
) -> Chart:
    """ Fetches chart's data.

    Args:
        request (Chart.Request):
            Example :
                request = Chart.Request()
                request.requestid = '1'
                request.resolution = Chart.Resolution.PT1M
                request.culture = 'fr-FR'
                request.series.append('issueid:360148977')
                request.series.append('price:issueid:360148977')
                request.series.append('ohlc:issueid:360148977')
                request.series.append('volume:issueid:360148977')
                request.period = Chart.Period.P1D
                request.tz = 'Europe/Paris'
        user_token (int):
            User identifier in Degiro's API.
        override (Dict[str], optional):
            Overrides the request sent to Degiro's API.
            Example :
                override = {
                    'period':'P6D',
                }
            Defaults to None.
        raw (bool, optional):
            Whether are not we want the raw API response.
            Defaults to False.
        session (requests.Session, optional):
            This object will be generated if None.
            Defaults to None.
        logger (logging.Logger, optional):
            This object will be generated if None.
            Defaults to None.

    Returns:
        Chart: Data of the chart.
    """

    if logger is None:
        logger = build_logger()
    if session is None:
        session = build_session()

    url = urls.CHART
    params = pb_handler.chart_request_to_api(request=request)
    params['format'] = 'json'
    params['callback'] = ''
    params['userToken'] = user_token

    if override is not None:
        for key, value in override.items():
            params[key] = value

    request = requests.Request(method='GET', url=url, params=params)
    prepped = session.prepare_request(request)
    response_raw = None

    try:
        response_raw = session.send(prepped, verify=False)
        response_dict = json.loads(response_raw.text)

        if raw is True:
            response = response_dict
        else:
            response = pb_handler.api_to_chart(payload=response_dict)

    except Exception as e:
        logger.fatal(response_raw.status_code)
        logger.fatal(response_raw.text)
        logger.fatal(e)
        return False

    return response
