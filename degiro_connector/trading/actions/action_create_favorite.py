import logging

import requests

from degiro_connector.core.constants import urls
from degiro_connector.core.abstracts.abstract_action import AbstractAction
from degiro_connector.trading.models.credentials import Credentials
from degiro_connector.trading.models.favorite import FavoriteId, FavoriteName


class ActionCreateFavoriteList(AbstractAction):
    @classmethod
    def favorite_list_to_api(cls, name: str) -> dict[str, str]:
        return {"name": name}

    @classmethod
    def api_to_favorite_list_id(cls, response_dict: dict[str, int]) -> int:
        return response_dict["data"]

    @classmethod
    def create_favorite_list(
        cls,
        name: str,
        session_id: str,
        credentials: Credentials,
        session: requests.Session | None = None,
        logger: logging.Logger | None = None,
    ) -> int | None:
        """Create a favorite list.
        Args:
            name (str):
                New name of the favorite list.
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
        url = urls.FAVOURITES_LIST

        params = {
            "intAccount": int_account,
            "sessionId": session_id,
        }

        json_obj = FavoriteName(name=name).model_dump(
            mode="python", by_alias=True, exclude_none=True
        )

        request = requests.Request(
            method="POST",
            url=url,
            params=params,
            json=json_obj,
        )
        prepped = session.prepare_request(request)

        favorite_list_id = None
        try:
            response = session.send(prepped)
            response.raise_for_status()
            favorite_list_id = FavoriteId.model_validate_json(
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

        return favorite_list_id

    def call(
        self,
        name: str,
    ) -> int | None:
        connection_storage = self.connection_storage
        session_id = connection_storage.session_id
        session = self.session_storage.session
        credentials = self.credentials
        logger = self.logger

        return self.create_favorite_list(
            name=name,
            session_id=session_id,
            credentials=credentials,
            session=session,
            logger=logger,
        )
