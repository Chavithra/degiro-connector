# IMPORTATION STANDARD
import requests
import logging
import json
from typing import Optional

# IMPORTATION THIRD PARTY
# IMPORTATION INTERNAL
import degiro_connector.core.constants.urls as urls
from degiro_connector.core.abstracts.abstract_action import AbstractAction


class ActionConnect(AbstractAction):
    @classmethod
    def get_session_id(
        cls,
        user_token: int,
        logger: logging.Logger = None,
        session: requests.Session = None,
    ) -> Optional[str]:
        """Retrieves the "session_id" necessary to access the data-stream.
        Args:
            user_token (int):
                User identifier in Degiro's API.
            session (requests.Session, optional):
                This object will be generated if None.
                Defaults to None.
            logger (logging.Logger, optional):
                This object will be generated if None.
                Defaults to None.
        Returns:
            str: Session id
        """

        if logger is None:
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        url = urls.QUOTECAST
        url = f"{url}/request_session"
        version = urls.QUOTECAST_VERSION

        parameters = {"version": version, "userToken": user_token}
        data = '{"referrer":"https://trader.degiro.nl"}'

        request = requests.Request(method="POST", url=url, data=data, params=parameters)
        prepped = session.prepare_request(request=request)

        try:
            response = session.send(request=prepped, verify=False)
            response_dict = json.loads(response.text)
        except Exception as e:
            logger.fatal(e)
            return None

        logger.info("get_session_id:response_dict: %s", response_dict)

        if "sessionId" in response_dict:
            return response_dict["sessionId"]
        else:
            return None

    def call(self) -> Optional[str]:
        connection_storage = self.connection_storage
        session = self.session_storage.session
        credentials = self.credentials
        user_token = credentials["user_token"]
        logger = self.logger

        connection_storage.session_id = self.get_session_id(
            user_token=user_token,
            logger=logger,
            session=session,
        )

        return connection_storage.session_id
