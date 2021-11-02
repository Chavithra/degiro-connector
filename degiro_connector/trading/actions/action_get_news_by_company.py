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
    NewsByCompany,
)


class ActionGetNewsByCompany(AbstractAction):
    @staticmethod
    def news_by_company_request_to_api(
        request: NewsByCompany.Request,
    ) -> dict:
        request_dict = {
            "isin": request.isin,
            "limit": request.limit,
            "offset": request.offset,
            "languages": request.languages,
        }

        return request_dict

    @staticmethod
    def news_by_company_to_grpc(payload: dict) -> NewsByCompany:
        news_by_company = NewsByCompany()
        json_format.ParseDict(
            js_dict=payload["data"],
            message=news_by_company,
            ignore_unknown_fields=False,
            descriptor_pool=None,
        )

        return news_by_company

    @classmethod
    def get_news_by_company(
        cls,
        request: NewsByCompany.Request,
        session_id: str,
        credentials: Credentials,
        raw: bool = False,
        session: requests.Session = None,
        logger: logging.Logger = None,
    ) -> Union[NewsByCompany, Dict, None]:
        if logger is None:
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        url = urls.NEWS_BY_COMPANY

        params = cls.news_by_company_request_to_api(
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
                return cls.news_by_company_to_grpc(
                    payload=response_dict,
                )
        except Exception as e:
            logger.fatal("error")
            logger.fatal(response_raw)
            logger.fatal(e)
            return None

    def call(
        self,
        request: NewsByCompany.Request,
        raw: bool = False,
    ) -> Union[NewsByCompany, Dict, None]:
        connection_storage = self.connection_storage
        session_id = connection_storage.session_id
        session = self.session_storage.session
        credentials = self.credentials
        logger = self.logger

        return self.get_news_by_company(
            request=request,
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )
