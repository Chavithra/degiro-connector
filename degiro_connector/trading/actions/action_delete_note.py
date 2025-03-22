import logging

import requests

from degiro_connector.core.constants import urls
from degiro_connector.core.abstracts.abstract_action import AbstractAction
from degiro_connector.trading.models.credentials import Credentials


class ActionDeleteNote(AbstractAction):
    @classmethod
    def delete_favorite(
        cls,
        note_id: int,
        session_id: str,
        credentials: Credentials,
        session: requests.Session | None = None,
        logger: logging.Logger | None = None,
    ) -> bool | None:
        """Delete a favorite list.
        Args:
            note_id (int):
                Note id.
            session_id (str):
                API's session id.
            credentials (Credentials):
                Credentials containing the parameter "int_account".
            raw (bool, optional):
                Whether are not we want the raw API response.
                Defaults to False.
            session (requests.Session, optional):
                This object will be generated if None.
                Defaults to None.
            logger (logging.Logger, optional):
                This object will be generated if None.
                Defaults to None.
        Returns:
            Favorites: API response.
        """

        if logger is None:
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        int_account = credentials.int_account
        url = f"{urls.NOTES_LIST}/{note_id}"
        params = {"intAccount": int_account, "sessionId": session_id}

        request = requests.Request(method="DELETE", url=url, params=params)
        prepped = session.prepare_request(request)

        try:
            response = session.send(prepped)
            response.raise_for_status()
        except requests.HTTPError as e:
            logger.fatal(e)
            if isinstance(e.response, requests.Response):
                logger.fatal(e.response.text)
            return None
        except Exception as e:
            logger.fatal(e)
            return None

        return response.status_code == 200

    def call(
        self,
        note_id: int,
    ) -> bool | None:
        connection_storage = self.connection_storage
        session_id = connection_storage.session_id
        session = self.session_storage.session
        credentials = self.credentials
        logger = self.logger

        return self.delete_favorite(
            note_id=note_id,
            session_id=session_id,
            credentials=credentials,
            session=session,
            logger=logger,
        )
