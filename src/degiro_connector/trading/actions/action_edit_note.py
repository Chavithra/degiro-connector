import logging

import requests

from degiro_connector.core.constants import urls
from degiro_connector.core.abstracts.abstract_action import AbstractAction
from degiro_connector.trading.models.credentials import Credentials
from degiro_connector.trading.models.note import NoteEditRequest, NoteEditResponse, NoteItem


class ActionEditNote(AbstractAction):
    @classmethod
    def edit_note(
        cls,
        note: NoteEditRequest,
        session_id: str,
        credentials: Credentials,
        session: requests.Session | None = None,
        logger: logging.Logger | None = None,
    ) -> NoteItem | None:
        """Create a favorite list.
        Args:
            note (NoteAdd):
                New note details.
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
            Modified note: API response.
        """

        if logger is None:
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        int_account = credentials.int_account
        url = f"{urls.NOTES_LIST}/{note.note_id}"

        params = {
            "intAccount": int_account,
            "sessionId": session_id,
        }

        json_map = note.model_dump(
            by_alias=True,
            exclude={"note_id"},
            exclude_none=True,
            mode="json",
        )

        request = requests.Request(
            method="PUT",
            url=url,
            params=params,
            json=json_map,
        )
        prepped = session.prepare_request(request)

        print(json_map)

        modified_note = None
        try:
            response = session.send(prepped)
            response.raise_for_status()
            modified_note = NoteEditResponse.model_validate_json(json_data=response.text).data
        except requests.HTTPError as e:
            logger.fatal(e)
            if isinstance(e.response, requests.Response):
                logger.fatal(e.response.text)
            return None
        except Exception as e:
            logger.fatal(e)
            return None

        return modified_note

    def call(
        self,
        note: NoteEditRequest,
    ) -> NoteItem | None:
        connection_storage = self.connection_storage
        session_id = connection_storage.session_id
        session = self.session_storage.session
        credentials = self.credentials
        logger = self.logger

        return self.edit_note(
            note=note,
            session_id=session_id,
            credentials=credentials,
            session=session,
            logger=logger,
        )
