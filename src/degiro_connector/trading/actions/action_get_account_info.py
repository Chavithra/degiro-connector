import logging

import requests
from orjson import loads

from degiro_connector.core.constants import urls
from degiro_connector.core.abstracts.abstract_action import AbstractAction
from degiro_connector.trading.models.credentials import Credentials


class ActionGetAccountInfo(AbstractAction):
    @classmethod
    def get_account_info(
        cls,
        session_id: str,
        credentials: Credentials,
        session: requests.Session | None = None,
        logger: logging.Logger | None = None,
    ) -> dict | None:
        if logger is None:
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        int_account = credentials.int_account
        url = f"{urls.ACCOUNT_INFO}/{int_account};jsessionid={session_id}"

        request = requests.Request(method="GET", url=url)
        prepped = session.prepare_request(request)

        try:
            response = session.send(prepped)
            response.raise_for_status()
            model = loads(response.text)

            return model
        except requests.HTTPError as e:
            logger.fatal(e)
            if isinstance(e.response, requests.Response):
                logger.fatal(e.response.text)
            return None
        except Exception as e:
            logger.fatal(e)
            return None

    def call(self) -> dict | None:
        connection_storage = self.connection_storage
        session_id = connection_storage.session_id
        session = self.session_storage.session
        credentials = self.credentials
        logger = self.logger

        return self.get_account_info(
            session_id=session_id,
            credentials=credentials,
            session=session,
            logger=logger,
        )
