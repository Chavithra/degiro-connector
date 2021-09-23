# IMPORTATION STANDARD
import requests
import logging
from typing import Dict

# IMPORTATION THIRD PARTY
import orjson as json
from google.protobuf import json_format

# IMPORTATION INTERNAL
import degiro_connector.core.constants.urls as urls
from degiro_connector.trading.models.trading_pb2 import (
    Credentials,
)
from degiro_connector.core.abstracts.abstract_action import AbstractAction


class ActionLogout(AbstractAction):
    @classmethod
    def logout(
        cls,
        credentials: Credentials,
        session_id: str,
        logger: logging.Logger = None,
        session: requests.Session = None,
    ) -> bool:
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
        response = None

        try:
            response = session.send(prepped, verify=False)
        except Exception as e:
            logger.fatal(response.status_code)
            logger.fatal(response.text)
            logger.fatal(e)
            return False

        return response.status_code == 200

    def call(self):
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
