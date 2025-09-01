import logging

import requests

from degiro_connector.core.constants import urls
from degiro_connector.core.abstracts.abstract_action import AbstractAction
from degiro_connector.trading.models.credentials import Credentials


class ActionDeleteOrder(AbstractAction):
    @classmethod
    def delete_order(
        cls,
        order_id: str,
        session_id: str,
        credentials: Credentials,
        session: requests.Session | None = None,
        logger: logging.Logger | None = None,
    ) -> bool | None:
        if logger is None:
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        int_account = credentials.int_account
        url = urls.ORDER_DELETE
        url = f"{url}/{order_id};jsessionid={session_id}"
        params = {"intAccount": int_account, "sessionId": session_id}

        request = requests.Request(method="DELETE", url=url, params=params)
        prepped = session.prepare_request(request)

        try:
            response = session.send(prepped)
            response.raise_for_status()

            return response.status_code == 200
        except requests.HTTPError as e:
            logger.fatal(e)
            if isinstance(e.response, requests.Response):
                logger.fatal(e.response.text)
            return None
        except Exception as e:
            logger.fatal(e)
            return None

    def call(
        self,
        order_id: str,
    ) -> bool | None:
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
