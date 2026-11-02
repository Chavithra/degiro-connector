import logging

import requests
from orjson import loads
from pydantic import TypeAdapter

from degiro_connector.core.constants import urls
from degiro_connector.core.abstracts.abstract_action import AbstractAction
from degiro_connector.trading.models.credentials import Credentials
from degiro_connector.trading.models.portfolio import (
    PortfolioReturn,
    PortfolioReturnRequest,
)


class ActionGetPortfolioReturn(AbstractAction):
    @staticmethod
    def build_model(response: requests.Response) -> list[PortfolioReturn]:
        model = TypeAdapter(list[PortfolioReturn]).validate_json(response.text)

        return model

    @staticmethod
    def build_params_map(
        portfolio_return_request: PortfolioReturnRequest,
    ) -> dict:
        params_map = portfolio_return_request.model_dump(
            by_alias=True,
            exclude_none=True,
            mode="json",
        )

        return params_map

    @classmethod
    def get_portfolio_return(
        cls,
        portfolio_return_request: PortfolioReturnRequest,
        session_id: str,
        credentials: Credentials,
        raw: bool = False,
        session: requests.Session | None = None,
        logger: logging.Logger | None = None,
    ) -> list[PortfolioReturn] | list | None:
        """Retrieve the portfolio return for a period.
        Args:
            portfolio_return_request (PortfolioReturnRequest):
                Period to retrieve.
                Example :
                    portfolio_return_request = PortfolioReturnRequest(
                        period=Period.YTD,
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
            list[PortfolioReturn]: API response.
        """

        if logger is None:
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        int_account = credentials.int_account
        url = urls.PORTFOLIO_RETURN
        params_map = cls.build_params_map(
            portfolio_return_request=portfolio_return_request
        )
        params_map.update({"intAccount": int_account, "sessionId": session_id})

        request = requests.Request(method="GET", url=url, params=params_map)
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
        portfolio_return_request: PortfolioReturnRequest,
        raw: bool = False,
    ) -> list[PortfolioReturn] | list | None:
        connection_storage = self.connection_storage
        session_id = connection_storage.session_id
        session = self.session_storage.session
        credentials = self.credentials
        logger = self.logger

        return self.get_portfolio_return(
            portfolio_return_request=portfolio_return_request,
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )
