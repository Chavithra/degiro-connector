# IMPORTATION STANDARD
import requests
import logging

# IMPORTATION THIRD PARTY

# IMPORTATION INTERNAL
import degiro_connector.core.constants.urls as urls
from degiro_connector.core.abstracts.abstract_action import AbstractAction


class ActionGetConfig(AbstractAction):
    @classmethod
    def get_config(
        cls,
        session_id: str,
        session: requests.Session = None,
        logger: logging.Logger = None,
    ) -> dict:
        if logger is None:
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        url = urls.CONFIG

        request = requests.Request(method="GET", url=url)
        prepped = session.prepare_request(request)
        prepped.headers["cookie"] = "JSESSIONID=" + session_id

        try:
            response = session.send(prepped, verify=False)
            response = response.json()
        except Exception as e:
            logger.fatal(e)
            return False

        if type(response) != dict:
            return False

        return response.get("data", False)

    def call(self):
        connection_storage = self.connection_storage
        session_id = connection_storage.session_id
        session = self.session_storage.session
        logger = self.logger

        return self.get_config(
            session_id=session_id,
            logger=logger,
            session=session,
        )
