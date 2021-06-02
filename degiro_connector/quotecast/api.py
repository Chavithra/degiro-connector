import logging
import urllib3

from degiro_connector.quotecast.basic import Basic
from degiro_connector.quotecast.models.connection_storage import (
    ConnectionStorage
)
from degiro_connector.quotecast.models.quotecast_parser import QuotecastParser
from degiro_connector.quotecast.pb.quotecast_pb2 import Chart, Quotecast
from typing import Dict, Union

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class API:
    """ Tools to consume Degiro's QuoteCast API.

    Same operations than "Basic" but with "session_id" management.

    Additional methods :
        * fetch_metrics

    This class should be threadsafe.
    """

    @property
    def basic(self) -> Basic:
        return self._basic

    @property
    def connection_storage(self) -> ConnectionStorage:
        return self._connection_storage

    @property
    def user_token(self) -> int:
        return self._basic.user_token

    def __init__(self, user_token: int):
        self._basic = Basic(user_token=user_token)

        self._connection_storage = ConnectionStorage(
            connection_timeout=15,
        )
        self._connection_storage.setup_hooks(
            session=self._basic.session_storage.session,
        )
        self._logger = logging.getLogger(self.__module__)

    def connect(self) -> str:
        basic = self.basic
        connection_storage = self._connection_storage
        connection_storage.session_id = basic.get_session_id()

        return connection_storage.session_id

    def fetch_data(self) -> Quotecast:
        basic = self.basic
        session_id = self.connection_storage.session_id

        return basic.fetch_data(
            session_id=session_id
        )

    def fetch_metrics(
        self,
        request: Quotecast.Request,
    ) -> Dict[
        Union[str, int],  # VWD_ID
        Dict[str, Union[str, int]]  # METRICS : NAME / VALUE
    ]:
        """ Fetch metrics from a request.

        If you seek realtime it's better to use "fetch_data".
        Since "fetch_data" consumes less ressources.

        Args:
            request (QuotecastAPI.Request):
                List of subscriptions & unsubscriptions to do.

        Returns:
            Dict[Union[str, int], Dict[str, Union[str, int]]]:
                Dict containing all the metrics grouped by "vwd_id".
        """

        logger = self._logger

        connection_attempts = 0
        ticker_dict = dict()
        while connection_attempts < 2:
            try:
                self.subscribe(request=request)
                quotecast = self.fetch_data()
                quotecast_parser = QuotecastParser(forward_fill=True)
                quotecast_parser.put_quotecast(quotecast=quotecast)
                ticker_dict = quotecast_parser.ticker_dict
                break
            except (ConnectionError, BrokenPipeError, TimeoutError) as e:
                logger.info(e)
                self.connect()
                connection_attempts += 1
            except Exception as e:
                logger.fatal(e)
                break

        return ticker_dict

    def get_chart(
        self,
        request: Chart.Request,
        override: Dict[str, str] = None,
        raw: bool = False,
    ) -> Chart:
        basic = self.basic

        return basic.get_chart(
            request=request,
            override=override,
            raw=raw,
        )

    def subscribe(self, request: Quotecast.Request) -> bool:
        basic = self.basic
        session_id = self._connection_storage.session_id

        return basic.subscribe(
            request=request,
            session_id=session_id,
        )


if __name__ == '__main__':
    # IMPORTATIONS
    import json
    import time

    # SETUP LOGS
    logging.basicConfig(level=logging.DEBUG)

    # SETUP CREDENTIALS
    with open('config/subscription_request.json') as config_file:
        config = json.load(config_file)
    user_token = config['user_token']

    # SETUP API
    api = API(user_token=user_token)

    # SETUP REQUEST
    request = Quotecast.Request()
    request.subscriptions['360015751'].extend([
        'LastDate',
        'LastTime',
        'LastPrice',
        'LastVolume',
    ])

    # CONNECT
    api.connect()

    # SUBSCRIBE
    api.subscribe(request=request)

    # FETCH DATA
    time.sleep(1)
    api.fetch_data()
