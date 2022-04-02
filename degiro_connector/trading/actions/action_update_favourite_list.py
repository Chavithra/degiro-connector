# IMPORTATION STANDARD
import logging
from typing import Dict, Optional

# IMPORTATION THIRD PARTY
import requests

# IMPORTATION INTERNAL
import degiro_connector.core.constants.urls as urls
from degiro_connector.core.abstracts.abstract_action import AbstractAction
from degiro_connector.trading.models.trading_pb2 import (
    Credentials,
)


class ActionUpdateFavouriteList(AbstractAction):
    @classmethod
    def favorite_list_to_api(cls, name: str) -> Dict[str, str]:
        return {"name":name}

    @classmethod
    def update_favourite_list(
        cls,
        id: int,
        name: str,
        session_id: str,
        credentials: Credentials,
        session: requests.Session = None,
        logger: logging.Logger = None,
    ) -> Optional[int]:
        """Update a favourite list.
        Args:
            id (str):
                Id of the favorite list to update.
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
            Favourites: API response.
        """

        if logger is None:
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        int_account = credentials.int_account
        url = f"{urls.PRODUCT_FAVOURITES_LISTS}/{id}"

        params = {
            "intAccount": int_account,
            "sessionId": session_id,
        }

        favorite_list_dict = cls.favorite_list_to_api(name=name)

        request = requests.Request(
            method="PUT",
            url=url,
            params=params,
            json=favorite_list_dict,
        )
        prepped = session.prepare_request(request)
        response_raw = None

        try:
            response_raw = session.send(prepped, verify=False)
            response_raw.raise_for_status()
        except requests.HTTPError as e:
            status_code = getattr(response_raw, "status_code", "No status_code found.")
            text = getattr(response_raw, "text", "No text found.")
            logger.fatal(status_code)
            logger.fatal(text)
            return None
        except Exception as e:
            logger.fatal(e)
            return None

        return response_raw.status_code == 200

    def call(
        self,
        id: int,
        name: str,
    ) -> Optional[int]:
        connection_storage = self.connection_storage
        session_id = connection_storage.session_id
        session = self.session_storage.session
        credentials = self.credentials
        logger = self.logger

        return self.update_favourite_list(
            id=id,
            name=name,
            session_id=session_id,
            credentials=credentials,
            session=session,
            logger=logger,
        )
