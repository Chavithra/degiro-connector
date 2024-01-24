import logging

import requests
from orjson import loads
from pydantic import TypeAdapter

from degiro_connector.core.constants import urls
from degiro_connector.core.abstracts.abstract_action import AbstractAction
from degiro_connector.trading.models.credentials import Credentials
from degiro_connector.trading.models.product_search import (
    Underlying,
    UnderlyingsRequest,
)


class ActionGetUnderlyings(AbstractAction):
    @staticmethod
    def build_model(response: requests.Response) -> list[Underlying]:
        model = TypeAdapter(list[Underlying]).validate_json(response.text)

        return model

    @staticmethod
    def build_params_map(underlyings_request: UnderlyingsRequest) -> dict:
        params_map = underlyings_request.model_dump(
            by_alias=True,
            exclude_none=True,
            mode="json",
        )

        return params_map

    @staticmethod
    def get_url(underlyings_request: UnderlyingsRequest) -> str:
        if underlyings_request.future_exchange_id:
            url = urls.FUTURES_UNDERLYINGS
        else:
            url = urls.OPTIONS_UNDERLYINGS

        return url

    @classmethod
    def get_underlyings(
        cls,
        session_id: str,
        credentials: Credentials,
        underlyings_request: UnderlyingsRequest,
        raw: bool = False,
        session: requests.Session | None = None,
        logger: logging.Logger | None = None,
    ) -> list[Underlying] | dict | None:
        """Retrieve information about the account.
        Args:
            underlyings_request (int):
                Example:
                    underlyings_request= UnderlyingsRequest(
                        # future_exchange_id=1,
                        option_exchange_id=3,
                    ),
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
            list[Underlying]: API response.
        """

        if logger is None:
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        int_account = credentials.int_account
        url = cls.get_url(underlyings_request=underlyings_request)
        params_map = cls.build_params_map(underlyings_request=underlyings_request)
        params_map.update({"intAccount": int_account, "sessionId": session_id})

        request = requests.Request(
            method="GET",
            params=params_map,
            url=url,
        )
        prepped = session.prepare_request(request=request)

        try:
            response = session.send(prepped)
            response.raise_for_status()

            if raw is True:
                model = loads(response.text)
            else:
                model = cls.build_model(response=response)
            return model
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
        underlyings_request: UnderlyingsRequest,
        raw: bool = False,
    ) -> list[Underlying] | dict | None:
        connection_storage = self.connection_storage
        session_id = connection_storage.session_id
        session = self.session_storage.session
        credentials = self.credentials
        logger = self.logger

        return self.get_underlyings(
            underlyings_request=underlyings_request,
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )
