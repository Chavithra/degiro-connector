# IMPORTATION STANDARD
import logging
from typing import Optional

# IMPORTATION THIRD PARTY
import requests

# IMPORTATION INTERNAL
import degiro_connector.core.constants.urls as urls
from degiro_connector.core.abstracts.abstract_action import AbstractAction
from degiro_connector.trading.models.trading_pb2 import (
    Credentials,
)


class ActionGetAccountInfo(AbstractAction):
    @classmethod
    def get_account_info(
        cls,
        session_id: str,
        credentials: Credentials,
        session: requests.Session = None,
        logger: logging.Logger = None,
    ) -> Optional[dict]:
        if logger is None:
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        int_account = credentials.int_account
        url = f"{urls.ACCOUNT_INFO}/{int_account};jsessionid={session_id}"

        request = requests.Request(method="GET", url=url)
        prepped = session.prepare_request(request)

        try:
            response_raw = session.send(prepped, verify=False)
            response_raw.raise_for_status()
            response_dict = response_raw.json()
        except requests.HTTPError as e:
            status_code = getattr(response_raw, "status_code", "No status_code found.")
            text = getattr(response_raw, "text", "No text found.")
            logger.fatal(status_code)
            logger.fatal(text)
            return None
        except Exception as e:
            logger.fatal(e)
            return None

        return response_dict

    def call(self) -> Optional[dict]:
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
