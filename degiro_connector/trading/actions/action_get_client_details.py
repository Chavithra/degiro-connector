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
        response = session.send(prepped, verify=False)

        if response.status_code != 200:
            return None

        response = response.json()

        if type(response) != dict:
            return None

        return response

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
