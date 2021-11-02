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
    TopNewsPreview,
)


class ActionGetTopNewsPreview(AbstractAction):
    @staticmethod
    def top_news_preview_to_grpc(payload: dict) -> TopNewsPreview:
        top_news_preview = TopNewsPreview()
        json_format.ParseDict(
            js_dict=payload["data"],
            message=top_news_preview,
            ignore_unknown_fields=False,
            descriptor_pool=None,
        )

        return top_news_preview

    @classmethod
    def get_top_news_preview(
        cls,
        session_id: str,
        credentials: Credentials,
        raw: bool = False,
        session: requests.Session = None,
        logger: logging.Logger = None,
    ) -> Union[TopNewsPreview, Dict, None]:
        if logger is None:
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        url = urls.TOP_NEWS_PREVIEW

        params = {
            "intAccount": credentials.int_account,
            "sessionId": session_id,
        }

        request = requests.Request(method="GET", url=url, params=params)
        prepped = session.prepare_request(request)
        prepped.headers["cookie"] = "JSESSIONID=" + session_id

        response_raw = None

        try:
            response_raw = session.send(prepped, verify=False)
            response_raw.raise_for_status()
            response_dict = response_raw.json()

            if raw is True:
                return response_dict
            else:
                return cls.top_news_preview_to_grpc(
                    payload=response_dict,
                )
        except Exception as e:
            logger.fatal("error")
            logger.fatal(response_raw)
            logger.fatal(e)
            return None

    def call(
        self,
        raw: bool = False,
    ) -> Union[TopNewsPreview, Dict, None]:
        connection_storage = self.connection_storage
        session_id = connection_storage.session_id
        session = self.session_storage.session
        credentials = self.credentials
        logger = self.logger

        return self.get_top_news_preview(
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )
