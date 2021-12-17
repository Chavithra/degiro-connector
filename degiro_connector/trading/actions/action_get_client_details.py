# IMPORTATION STANDARD
import logging
from typing import Dict, Union

# IMPORTATION THIRD PARTY
import requests

# IMPORTATION INTERNAL
import degiro_connector.core.constants.urls as urls
from degiro_connector.core.abstracts.abstract_action import AbstractAction


class ActionGetClientDetails(AbstractAction):
    @classmethod
    def get_client_details(
        cls,
        session_id: str,
        session: requests.Session = None,
        logger: logging.Logger = None,
    ) -> Union[Dict, None]:
        if logger is None:
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        url = urls.CLIENT_DETAILS

        params = {
            "sessionId": session_id,
        }

        request = requests.Request(method="GET", url=url, params=params)
        prepped = session.prepare_request(request)
        response_raw = None

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

    def call(self) -> Union[Dict, None]:
        connection_storage = self.connection_storage
        session_id = connection_storage.session_id
        session = self.session_storage.session
        logger = self.logger

        return self.get_client_details(
            session_id=session_id,
            session=session,
            logger=logger,
        )
