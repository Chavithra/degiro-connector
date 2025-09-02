import logging


import requests
from orjson import loads

from degiro_connector.core.constants import urls
from degiro_connector.core.abstracts.abstract_action import AbstractAction
from degiro_connector.trading.models.credentials import Credentials
from degiro_connector.trading.models.news import BatchWrapper, NewsBatch, NewsRequest


class ActionGetNewsByCompany(AbstractAction):
    @staticmethod
    def build_params_map(news_request: NewsRequest) -> dict:
        params_map = news_request.model_dump(
            by_alias=True,
            exclude_none=True,
            mode="json",
        )

        return params_map

    @classmethod
    def get_news_by_company(
        cls,
        news_request: NewsRequest,
        session_id: str,
        credentials: Credentials,
        raw: bool = False,
        session: requests.Session | None = None,
        logger: logging.Logger | None = None,
    ) -> NewsBatch | dict | None:
        if logger is None:
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        int_account = credentials.int_account
        url = urls.NEWS_BY_COMPANY
        params_map = cls.build_params_map(news_request=news_request)
        params_map.update({"intAccount": int_account, "sessionId": session_id})

        http_request = requests.Request(method="GET", url=url, params=params_map)
        prepped = session.prepare_request(http_request)
        prepped.headers["cookie"] = "JSESSIONID=" + session_id

        response_raw = None

        try:
            response = session.send(prepped)
            response.raise_for_status()

            if raw is True:
                company_news = loads(response.text)
            else:
                company_news = BatchWrapper.model_validate_json(
                    json_data=response.text
                ).data

            return company_news
        except Exception as e:
            logger.fatal(e)
            logger.fatal(response_raw)
            return None

    def call(
        self,
        news_request: NewsRequest,
        raw: bool = False,
    ) -> NewsBatch | dict | None:
        connection_storage = self.connection_storage
        session_id = connection_storage.session_id
        session = self.session_storage.session
        credentials = self.credentials
        logger = self.logger

        return self.get_news_by_company(
            news_request=news_request,
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )
