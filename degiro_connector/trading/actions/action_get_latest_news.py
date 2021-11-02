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
    LatestNews,
)


class ActionGetLatestNews(AbstractAction):
    @staticmethod
    def latest_news_request_to_api(
        request: LatestNews.Request,
    ) -> dict:
        request_dict = {
            "offset": request.offset,
            "languages": request.languages,
            "limit": request.limit,
        }

        return request_dict

    @staticmethod
    def latest_news_to_grpc(payload: dict) -> LatestNews:
        latest_news = LatestNews()
        json_format.ParseDict(
            js_dict=payload["data"],
            message=latest_news,
            ignore_unknown_fields=False,
            descriptor_pool=None,
        )

        return latest_news

    @classmethod
    def get_latest_news(
        cls,
        request: LatestNews.Request,
        session_id: str,
        credentials: Credentials,
        raw: bool = False,
        session: requests.Session = None,
        logger: logging.Logger = None,
    ) -> Union[LatestNews, Dict, None]:
        if logger is None:
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        url = urls.LATEST_NEWS

        params = cls.latest_news_request_to_api(
            request=request,
        )
        params["intAccount"] = credentials.int_account
        params["sessionId"] = session_id

        http_request = requests.Request(method="GET", url=url, params=params)
        prepped = session.prepare_request(http_request)
        prepped.headers["cookie"] = "JSESSIONID=" + session_id

        response_raw = None

        try:
            response_raw = session.send(prepped, verify=False)
            response_raw.raise_for_status()
            response_dict = response_raw.json()

            if raw is True:
                return response_dict
            else:
                return cls.latest_news_to_grpc(
                    payload=response_dict,
                )
        except Exception as e:
            logger.fatal("error")
            logger.fatal(response_raw)
            logger.fatal(e)
            return None

    def call(
        self,
        request: LatestNews.Request,
        raw: bool = False,
    ) -> Union[LatestNews, Dict, None]:
        connection_storage = self.connection_storage
        session_id = connection_storage.session_id
        session = self.session_storage.session
        credentials = self.credentials
        logger = self.logger

        return self.get_latest_news(
            request=request,
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )
