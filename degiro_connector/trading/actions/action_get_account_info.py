# IMPORTATION STANDARD
import logging
from typing import Dict, Union

# IMPORTATION THIRD PARTY
import requests
from google.protobuf import json_format

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
    ) -> dict:
        if logger is None:
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        int_account = credentials.int_account
        url = f"{urls.ACCOUNT_INFO}/{int_account};jsessionid={session_id}"

        request = requests.Request(method="GET", url=url)
        prepped = session.prepare_request(request)
        response = session.send(prepped, verify=False)

        if response.status_code != 200:
            return False

        return response.json()

    def call(self) -> dict:
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
