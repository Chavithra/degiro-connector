import logging

import requests

from degiro_connector.core.constants import urls
from degiro_connector.core.abstracts.abstract_action import AbstractAction
from degiro_connector.trading.models.credentials import Credentials
from degiro_connector.trading.models.favourite import FavouriteId, FavouriteName


class ActionCreateFavouriteList(AbstractAction):
    @classmethod
    def favourite_list_to_api(cls, name: str) -> dict[str, str]:
        return {"name": name}

    @classmethod
    def api_to_favourite_list_id(cls, response_dict: dict[str, int]) -> int:
        return response_dict["data"]

    @classmethod
    def create_favourite_list(
        cls,
        name: str,
        session_id: str,
        credentials: Credentials,
        session: requests.Session | None = None,
        logger: logging.Logger | None = None,
    ) -> int | None:
        """Create a favourite list.
        Args:
            name (str):
                New name of the favourite list.
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
            Favourites: API response.
        """

        if logger is None:
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        int_account = credentials.int_account
        url = urls.FAVOURITES_LIST

        params = {
            "intAccount": int_account,
            "sessionId": session_id,
        }

        json_obj = FavouriteName(name=name).model_dump(
            mode="python", by_alias=True, exclude_none=True
        )

        request = requests.Request(
            method="POST",
            url=url,
            params=params,
            json=json_obj,
        )
        prepped = session.prepare_request(request)

        favourite_list_id = None
        try:
            response = session.send(prepped)
            response.raise_for_status()
            favourite_list_id = FavouriteId.model_validate_json(
                json_data=response.text
            ).data
        except requests.HTTPError as e:
            logger.fatal(e)
            if isinstance(e.response, requests.Response):
                logger.fatal(e.response.text)
            return None
        except Exception as e:
            logger.fatal(e)
            return None

        return favourite_list_id

    def call(
        self,
        name: str,
    ) -> int | None:
        connection_storage = self.connection_storage
        session_id = connection_storage.session_id
        session = self.session_storage.session
        credentials = self.credentials
        logger = self.logger

        return self.create_favourite_list(
            name=name,
            session_id=session_id,
            credentials=credentials,
            session=session,
            logger=logger,
        )
