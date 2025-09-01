import logging


import requests
from orjson import loads

from degiro_connector.core.constants import urls
from degiro_connector.core.abstracts.abstract_action import AbstractAction
from degiro_connector.trading.models.credentials import Credentials
from degiro_connector.trading.models.news import (
    LatestNews,
    LatestRequest,
    LatestWrapper,
)


class ActionGetLatestNews(AbstractAction):
    @staticmethod
    def build_model(response: requests.Response) -> LatestNews:
        model = LatestWrapper.model_validate_json(json_data=response.text).data

        return model

    @staticmethod
    def build_params_map(
        latest_request: LatestRequest,
    ) -> dict:
        params_map = latest_request.model_dump(
            by_alias=True,
            exclude_none=True,
            mode="json",
        )

        return params_map

    @classmethod
    def get_latest_news(
        cls,
        latest_request: LatestRequest,
        session_id: str,
        credentials: Credentials,
        raw: bool = False,
        session: requests.Session | None = None,
        logger: logging.Logger | None = None,
    ) -> LatestNews | dict | None:
        if logger is None:
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        int_account = credentials.int_account
        url = urls.LATEST_NEWS

        params_map = cls.build_params_map(latest_request=latest_request)
        params_map.update({"intAccount": int_account, "sessionId": session_id})

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
        latest_request: LatestRequest,
        raw: bool = False,
    ) -> LatestNews | dict | None:
        connection_storage = self.connection_storage
        session_id = connection_storage.session_id
        session = self.session_storage.session
        credentials = self.credentials
        logger = self.logger

        return self.get_latest_news(
            latest_request=latest_request,
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )
