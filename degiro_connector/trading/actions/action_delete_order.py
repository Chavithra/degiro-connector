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


class ActionDeleteOrder(AbstractAction):
    @classmethod
    def delete_order(
        cls,
        order_id: str,
        session_id: str,
        credentials: Credentials,
        session: requests.Session = None,
        logger: logging.Logger = None,
    ) -> Optional[bool]:
        if logger is None:
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        int_account = credentials.int_account
        url = urls.ORDER_DELETE
        url = f"{url}/{order_id};jsessionid={session_id}"

        params = {
            "intAccount": int_account,
            "sessionId": session_id,
        }

        request = requests.Request(method="DELETE", url=url, params=params)
        prepped = session.prepare_request(request)
        response_raw = None

        try:
            response_raw = session.send(prepped, verify=False)
            response_raw.raise_for_status()
        except requests.HTTPError as e:
            status_code = getattr(response_raw, "status_code", "No status_code found.")
            text = getattr(response_raw, "text", "No text found.")
            logger.fatal(status_code)
            logger.fatal(text)
            return None
        except Exception as e:
            logger.fatal(e)
            return None

        return response_raw.status_code == 200

    def call(
        self,
        order_id: str,
    ) -> Optional[bool]:
        connection_storage = self.connection_storage
        session_id = connection_storage.session_id
        session = self.session_storage.session
        credentials = self.credentials
        logger = self.logger

        return self.delete_order(
            order_id=order_id,
            session_id=session_id,
            credentials=credentials,
            session=session,
            logger=logger,
        )
