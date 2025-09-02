import logging

import requests
from orjson import loads

from degiro_connector.core.constants import urls
from degiro_connector.core.abstracts.abstract_action import AbstractAction
from degiro_connector.trading.models.credentials import Credentials
from degiro_connector.trading.models.product import (
    FinancialStatements,
    StatementsWrapper,
)


class ActionGetFinancialStatements(AbstractAction):
    @staticmethod
    def build_model(response: requests.Response) -> FinancialStatements:
        model = StatementsWrapper.model_validate_json(json_data=response.text).data

        return model

    @classmethod
    def get_financial_statements(
        cls,
        product_isin: str,
        session_id: str,
        credentials: Credentials,
        raw: bool = False,
        session: requests.Session | None = None,
        logger: logging.Logger | None = None,
    ) -> FinancialStatements | dict | None:
        if logger is None:
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        int_account = credentials.int_account
        url = f"{urls.FINANCIAL_STATEMENTS}/{product_isin}"
        params_map = {"intAccount": int_account, "sessionId": session_id}

        request = requests.Request(
            method="GET",
            params=params_map,
            url=url,
        )
        prepped = session.prepare_request(request)
        prepped.headers["cookie"] = "JSESSIONID=" + session_id

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
        product_isin: str,
        raw: bool = False,
    ) -> FinancialStatements | dict | None:
        connection_storage = self.connection_storage
        session_id = connection_storage.session_id
        session = self.session_storage.session
        credentials = self.credentials
        logger = self.logger

        return self.get_financial_statements(
            product_isin=product_isin,
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )
