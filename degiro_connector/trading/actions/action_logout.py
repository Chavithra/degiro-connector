import logging

import requests

from degiro_connector.core.constants import urls
from degiro_connector.trading.models.credentials import Credentials
from degiro_connector.core.abstracts.abstract_action import AbstractAction


class ActionLogout(AbstractAction):
    @classmethod
    def logout(
        cls,
        credentials: Credentials,
        session_id: str,
        logger: logging.Logger | None = None,
        session: requests.Session | None = None,
    ) -> bool | None:
        if logger is None:
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        int_account = credentials.int_account
        url = urls.LOGOUT
        url = f"{url};jsessionid={session_id}"

        params = {
            "intAccount": int_account,
            "sessionId": session_id,
        }

        request = requests.Request(
            method="PUT",
            url=url,
            params=params,
        )
        prepped = session.prepare_request(request)
        response_raw = None

        try:
            response_raw = session.send(prepped)
            response_raw.raise_for_status()
        except requests.HTTPError as e:
            logger.fatal(e)
            if isinstance(e.response, requests.Response):
                logger.fatal(e.response.text)
            status_code = getattr(response_raw, "status_code", "No status_code found.")
            text = getattr(response_raw, "text", "No text found.")
            logger.fatal(status_code)
            logger.fatal(text)
            return None
        except Exception as e:
            logger.fatal(e)
            return None

        return response_raw.status_code == 200

    def call(self) -> bool | None:
        connection_storage = self.connection_storage
        session_id = connection_storage.session_id
        session = self.session_storage.session
        logger = self.logger
        credentials = self.credentials

        return self.logout(
            credentials=credentials,
            session_id=session_id,
            logger=logger,
            session=session,
        )
