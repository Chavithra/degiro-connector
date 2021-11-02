# IMPORTATION STANDARD
import requests
import logging
from typing import Optional

# IMPORTATION THIRD PARTY
# IMPORTATION INTERNAL
import degiro_connector.core.constants.urls as urls
from degiro_connector.quotecast.models.quotecast_pb2 import (
    Quotecast,
)
from degiro_connector.core.abstracts.abstract_action import AbstractAction


class ActionSubscribe(AbstractAction):
    @staticmethod
    def quotecast_request_to_api(request: Quotecast.Request) -> str:
        payload = '{"controlData":"'
        for vwd_id in request.subscriptions:
            for metric_name in request.subscriptions[vwd_id]:
                payload += "a_req(" + vwd_id + "." + metric_name + ");"
        for vwd_id in request.unsubscriptions:
            for metric_name in request.unsubscriptions[vwd_id]:
                payload += "a_rel(" + vwd_id + "." + metric_name + ");"
        payload += '"}'

        return payload

    @classmethod
    def subscribe(
        cls,
        request: Quotecast.Request,
        session_id: str,
        session: requests.Session = None,
        logger: logging.Logger = None,
    ) -> Optional[bool]:
        """Adds/removes metric from the data-stream.
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
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        url = urls.QUOTECAST
        url = f"{url}/{session_id}"
        data = cls.quotecast_request_to_api(request=request)

        logger.info("subscribe:data %s", data[:100])

        session_request = requests.Request(method="POST", url=url, data=data)
        prepped = session.prepare_request(request=session_request)
        response_raw = None

        try:
            response_raw = session.send(request=prepped, verify=False)
            response_raw.raise_for_status()

            if response_raw.text == '[{"m":"sr"}]':
                raise BrokenPipeError('A new "session_id" is required.')
            else:
                return True
        except Exception as e:
            logger.fatal(e)
            return None

    def call(self, request: Quotecast.Request) -> Optional[bool]:
        session_id = self.connection_storage.session_id
        session = self.session_storage.session
        logger = self.logger

        return self.subscribe(
            request=request,
            session_id=session_id,
            session=session,
            logger=logger,
        )
