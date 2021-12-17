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
    Favourites,
)


class ActionGetFavouritesList(AbstractAction):
    @staticmethod
    def favourites_to_grpc(payload: dict) -> Favourites:
        favourites = Favourites()
        favourites.response_datetime.GetCurrentTime()
        json_format.ParseDict(
            js_dict={"values": payload["data"]},
            message=favourites,
            ignore_unknown_fields=False,
            descriptor_pool=None,
        )

        return favourites

    @classmethod
    def get_favourites_list(
        cls,
        session_id: str,
        credentials: Credentials,
        raw: bool = False,
        session: requests.Session = None,
        logger: logging.Logger = None,
    ) -> Union[Favourites, Dict, None]:
        """Retrieve the lists of favourite products.
        Args:
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
        url = urls.PRODUCT_FAVOURITES_LISTS

        params = {
            "intAccount": int_account,
            "sessionId": session_id,
        }

        request = requests.Request(method="GET", url=url, params=params)
        prepped = session.prepare_request(request)
        response_raw = None

        try:
            response_raw = session.send(prepped, verify=False)
            response_raw.raise_for_status()
            response_dict = response_raw.json()

            if raw is True:
                return response_dict
            else:
                return cls.favourites_to_grpc(
                    payload=response_dict,
                )
        except requests.HTTPError as e:
            status_code = getattr(response_raw, "status_code", "No status_code found.")
            text = getattr(response_raw, "text", "No text found.")
            logger.fatal(status_code)
            logger.fatal(text)
            return None
        except Exception as e:
            logger.fatal(e)
            return None

    def call(
        self,
        raw: bool = False,
    ) -> Union[Favourites, Dict, None]:
        connection_storage = self.connection_storage
        session_id = connection_storage.session_id
        session = self.session_storage.session
        credentials = self.credentials
        logger = self.logger

        return self.get_favourites_list(
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )
