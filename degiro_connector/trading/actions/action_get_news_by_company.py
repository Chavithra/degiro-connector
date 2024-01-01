import logging
from typing import Union

import requests
from orjson import loads

from degiro_connector.core.constants import urls
from degiro_connector.core.abstracts.abstract_action import AbstractAction
from degiro_connector.trading.models.credentials import Credentials
from degiro_connector.trading.models.news import BatchWrapper, NewsBatch, NewsRequest


class ActionGetNewsByCompany(AbstractAction):
    @classmethod
    def get_news_by_company(
        cls,
        news_request: NewsRequest,
        session_id: str,
        credentials: Credentials,
        raw: bool = False,
        session: requests.Session | None = None,
        logger: logging.Logger | None = None,
    ) -> Union[NewsBatch, dict, None]:
        if logger is None:
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        url = urls.NEWS_BY_COMPANY

        params = news_request.model_dump(
            mode="python", by_alias=True, exclude_none=True
        )
        params["intAccount"] = credentials.int_account
        params["sessionId"] = session_id

        http_request = requests.Request(method="GET", url=url, params=params)
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
    ) -> Union[NewsBatch, dict, None]:
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
