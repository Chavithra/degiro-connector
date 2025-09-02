import logging
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import requests
from orjson import loads

from degiro_connector.core.constants.urls import (
    QUOTECAST,
    QUOTECAST_VERSION,
)
from degiro_connector.core.constants.headers import HEADERS as HEADER_MAP
from degiro_connector.quotecast.models.ticker import Ticker, TickerRequest
from degiro_connector.quotecast.models.metric import MetricType


class TickerFetcher:
    @staticmethod
    def build_logger() -> logging.Logger:
        return logging.getLogger(__name__)

    @staticmethod
    def build_credentials(location: Path) -> dict[str, Any]:
        content = os.environ.get("DEGIRO_ACCOUNT") or location.read_text()
        config_dict = loads(content)

        return config_dict

    @staticmethod
    def build_session(
        headers: dict | None = None,
        hooks: dict | None = None,
    ) -> requests.Session:
        """Setup a "requests.Session" object.
        Args:
            headers (dict, optional):
                Headers to used for the Session.
                Defaults to None.
            hooks (dict, optional):
                Hooks for the Session.
                Defaults to None.

        Returns:
            requests.Session:
                Session object with the right headers and hooks.
        """

        session = requests.Session()

        if isinstance(headers, dict):
            session.headers.update(headers)
        else:
            session.headers.update(HEADER_MAP)

        if isinstance(hooks, dict):
            session.hooks.update(hooks)

        return session

    @classmethod
    def get_session_id(
        cls,
        user_token: int,
        logger: logging.Logger | None = None,
        session: requests.Session | None = None,
    ) -> str | None:
        """Retrieves the "session_id" necessary to access the data-stream.
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
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        url = QUOTECAST
        url = f"{url}/request_session"
        version = QUOTECAST_VERSION
        parameters = {"version": version, "userToken": user_token}
        data = '{"referrer":"https://trader.degiro.nl"}'
        request = requests.Request(method="POST", url=url, data=data, params=parameters)
        prepped = session.prepare_request(request=request)

        try:
            response = session.send(request=prepped)
            response_dict = loads(response.text)
        except Exception as e:
            logger.fatal(e)
            return None

        logger.info("get_session_id:response_dict: %s", response_dict)

        if "sessionId" in response_dict:
            return response_dict["sessionId"]
        else:
            return None

    @classmethod
    def fetch_ticker(
        cls,
        session_id: str,
        session: requests.Session | None = None,
        logger: logging.Logger | None = None,
    ) -> Ticker | None:
        """Fetches data from the feed.
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
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        url = f"{QUOTECAST}/{session_id}"
        request = requests.Request(method="GET", url=url)
        prepped = session.prepare_request(request=request)
        start_ns = time.perf_counter_ns()

        try:
            response = session.send(request=prepped)
            # We could have used : response.elapsed.total_seconds()
            duration_ns = time.perf_counter_ns() - start_ns

            if response.text == '[{"m":"sr"}]':
                raise BrokenPipeError('A new "session_id" is required.')

            ticker = Ticker(
                json_text=response.text,
                # There is no "date" header returned
                # We could have used : response.cookies._now
                response_datetime=datetime.now(),
                request_duration=timedelta(microseconds=duration_ns // 1000),
            )
        except requests.HTTPError as e:
            logger.fatal(e)
            if isinstance(e.response, requests.Response):
                logger.fatal(e.response.text)
            return None
        except Exception as e:
            logger.fatal(e)
            return None

        return ticker

    @staticmethod
    def build_ticker_request_payload(ticker_request: TickerRequest) -> str:
        """Build a payload like the following:
        '{"controlData":"a_req(360017018.LastDate);a_req(360017018.LastTime);a_req(360017018.LastPrice);"}'
        """

        request_map = ticker_request.request_map
        request_type = ticker_request.request_type
        request_function = "a_req" if (request_type == "subscription") else "a_rel"

        payload = '{"controlData":"'

        for product_id, metric_type_list in request_map.items():
            for metric_type in metric_type_list:
                if isinstance(metric_type, MetricType):
                    metric_name = metric_type.name
                else:
                    metric_name = metric_type
                payload += f"{request_function}({product_id}.{metric_name});"

        payload += '"}'

        return payload

    @classmethod
    def subscribe(
        cls,
        ticker_request: TickerRequest,
        session_id: str,
        session: requests.Session | None = None,
        logger: logging.Logger | None = None,
    ) -> bool | None:
        """Adds/removes metric from the data-stream.
        Args:
            ticker_request (TickerRequest):
                list of subscriptions & unsubscriptions to do.
                Example :
                    ticker_request: TickerRequest = TickerRequest(
                        request_type="subscription",
                        request_map={
                            "360017018" : [MetricType.LastDate, MetricType.LastPrice],
                            "AAPL.BATS,E" : [MetricType.LastPrice, MetricType.LastVolume],
                            "360015751" : [MetricType.LastPrice, MetricType.LastVolume],
                        },
                    )
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
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        url = QUOTECAST
        url = f"{url}/{session_id}"
        data = cls.build_ticker_request_payload(ticker_request=ticker_request)

        logger.info("subscribe:data %s", data[:100])

        session_request = requests.Request(method="POST", url=url, data=data)
        prepped = session.prepare_request(request=session_request)
        response = None

        try:
            response = session.send(request=prepped)
            response.raise_for_status()

            if response.text == '[{"m":"sr"}]':
                raise BrokenPipeError('A new "session_id" is required.')

            return True
        except requests.HTTPError as e:
            logger.fatal(e)
            if isinstance(e.response, requests.Response):
                logger.fatal(e.response.text)
            return None
        except Exception as e:
            logger.fatal(e)
            return None
