import logging

import requests
from orjson import loads

from degiro_connector.core.constants import urls
from degiro_connector.core.abstracts.abstract_action import AbstractAction
from degiro_connector.trading.models.credentials import Credentials
from degiro_connector.trading.models.news import (
    PreviewWrapper,
    PreviewRequest,
    TopNewsPreview,
)


class ActionGetTopNewsPreview(AbstractAction):
    @staticmethod
    def build_params_map(preview_request: PreviewRequest | None) -> dict:
        if preview_request:
            params_map = preview_request.model_dump(
                by_alias=True,
                exclude_none=True,
                mode="json",
            )
        else:
            params_map = {}

        return params_map

    @staticmethod
    def build_model(response: requests.Response) -> PreviewWrapper:
        model = PreviewWrapper.model_validate_json(json_data=response.text)

        return model

    @classmethod
    def get_top_news_preview(
        cls,
        session_id: str,
        credentials: Credentials,
        preview_request: PreviewRequest | None = None,
        product_list: list[int] | None = None,
        raw: bool = False,
        session: requests.Session | None = None,
        logger: logging.Logger | None = None,
    ) -> TopNewsPreview | dict | None:
        if logger is None:
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        int_account = credentials.int_account
        url = urls.TOP_NEWS_PREVIEW
        params_map = cls.build_params_map(preview_request=preview_request)
        params_map.update({"intAccount": int_account, "sessionId": session_id})

        request = requests.Request(
            json=product_list,
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
                model = cls.build_model(response=response).data
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
        preview_request: PreviewRequest | None = None,
        product_list: list[int] | None = None,
        raw: bool = False,
    ) -> TopNewsPreview | dict | None:
        connection_storage = self.connection_storage
        session_id = connection_storage.session_id
        session = self.session_storage.session
        credentials = self.credentials
        logger = self.logger

        return self.get_top_news_preview(
            preview_request=preview_request,
            product_list=product_list,
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )
