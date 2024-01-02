import logging

import requests
from orjson import loads

from degiro_connector.core.constants import urls
from degiro_connector.core.abstracts.abstract_action import AbstractAction
from degiro_connector.trading.models.credentials import Credentials
from degiro_connector.trading.models.product import ProductInfo


class ActionGetProductsInfo(AbstractAction):
    @staticmethod
    def build_model(response: requests.Response) -> ProductInfo:
        model = ProductInfo.model_validate_json(json_data=response.text)

        return model

    @classmethod
    def get_products_info(
        cls,
        product_list: list[int],
        session_id: str,
        credentials: Credentials,
        raw: bool = False,
        session: requests.Session | None = None,
        logger: logging.Logger | None = None,
    ) -> ProductInfo | dict | None:
        """Retrieve information about the account.
        Args:
            request (AccountOverview.Request):
                list of options that we want to retrieve from the endpoint.
                Example :
                    overview_request = OverviewRequest(
                        from_date=date(year=2023, month=10, day=15),
                        to_date=date(year=2024, month=1, day=1),
                    )
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
            AccountOverview: API response.
        """

        if logger is None:
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        int_account = credentials.int_account
        url = urls.PRODUCTS_INFO
        params_map = {"intAccount": int_account, "sessionId": session_id}

        request = requests.Request(
            json=product_list,
            method="POST",
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
        product_list: list[int],
        raw: bool = False,
    ) -> ProductInfo | dict | None:
        connection_storage = self.connection_storage
        session_id = connection_storage.session_id
        session = self.session_storage.session
        credentials = self.credentials
        logger = self.logger

        return self.get_products_info(
            product_list=product_list,
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )
