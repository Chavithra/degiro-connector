# IMPORTATION STANDARD
import requests
import logging
import time

# IMPORTATION THIRD PARTY
# IMPORTATION INTERNAL
import degiro_connector.core.constants.urls as urls
from degiro_connector.quotecast.models.quotecast_pb2 import (
    Quotecast,
)
from degiro_connector.core.abstracts.abstract_action import AbstractAction


class ActionFetchData(AbstractAction):
    @classmethod
    def fetch_data(
        cls,
        session_id: str,
        session: requests.Session = None,
        logger: logging.Logger = None,
    ) -> Quotecast:
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

        url = f"{urls.QUOTECAST}/{session_id}"

        request = requests.Request(method="GET", url=url)
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

    def call(self) -> Quotecast:
        session_id = self.connection_storage.session_id
        session = self.session_storage.session
        logger = self.logger

        return self.fetch_data(
            session_id=session_id,
            session=session,
            logger=logger,
        )
