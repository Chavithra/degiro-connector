import logging

import requests
from orjson import loads

from degiro_connector.core.constants import urls
from degiro_connector.core.abstracts.abstract_action import AbstractAction
from degiro_connector.trading.models.credentials import Credentials
from degiro_connector.trading.models.favorite import FavoriteBatch


class ActionGetFavorite(AbstractAction):
    @classmethod
    def get_favorite(
        cls,
        session_id: str,
        credentials: Credentials,
        raw: bool = False,
        session: requests.Session | None = None,
        logger: logging.Logger | None = None,
    ) -> FavoriteBatch | None:
        """Move a favorite list.
        Args:.
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

        params["sessionId"] = session_id

        http_request = requests.Request(method="GET", url=url, params=params)
        prepped = session.prepare_request(http_request)

        try:
            response = session.send(prepped)
            response.raise_for_status()

            if raw is True:
                favorite_batch = loads(response.text)
            else:
                favorite_batch = FavoriteBatch.model_validate_json(
                    json_data=response.text
                )

            return favorite_batch
        except requests.HTTPError as e:
            logger.fatal(e)
            if isinstance(e.response, requests.Response):
                logger.fatal(e.response.text)
            return None
        except Exception as e:
            logger.fatal(e)
            return None

    def call(
        self,
        raw: bool = False,
    ) -> FavoriteBatch | None:
        connection_storage = self.connection_storage
        session_id = connection_storage.session_id
        session = self.session_storage.session
        credentials = self.credentials
        logger = self.logger

        return self.get_favorite(
            raw=raw,
            session_id=session_id,
            credentials=credentials,
            session=session,
            logger=logger,
        )
