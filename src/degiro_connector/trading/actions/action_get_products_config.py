import logging


import requests
from orjson import loads

from degiro_connector.core.constants import urls
from degiro_connector.core.abstracts.abstract_action import AbstractAction
from degiro_connector.trading.models.credentials import Credentials


class ActionGetProductsConfig(AbstractAction):
    @classmethod
    def get_products_config(
        cls,
        session_id: str,
        credentials: Credentials,
        session: requests.Session | None = None,
        logger: logging.Logger | None = None,
    ) -> dict | None:
        """Fetch the product search config table.
        No credentials or logging seems to be required for this endpoint.
        Just adding the credentials and session_id because the website is
        doing it.
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
            ProductSearch.Config: API response.
        """

        if logger is None:
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        int_account = credentials.int_account
        url = urls.PRODUCT_SEARCH_DICTIONARY
        params = {"intAccount": int_account, "sessionId": session_id}

        request = requests.Request(method="GET", url=url, params=params)
        prepped = session.prepare_request(request)

        try:
            response = session.send(prepped)
            response.raise_for_status()

            model = loads(response.text)
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
    ) -> dict | None:
        connection_storage = self.connection_storage
        session_id = connection_storage.session_id
        session = self.session_storage.session
        credentials = self.credentials
        logger = self.logger

        return self.get_products_config(
            session_id=session_id,
            credentials=credentials,
            session=session,
            logger=logger,
        )
