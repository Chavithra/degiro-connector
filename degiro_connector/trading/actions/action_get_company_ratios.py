import logging
from typing import Union

import requests
from google.protobuf import json_format

from degiro_connector.core.constants import urls
from degiro_connector.core.abstracts.abstract_action import AbstractAction
from degiro_connector.trading.models.credentials import Credentials
from degiro_connector.trading.models.trading_pb2 import (
    CompanyRatios,
)


class ActionGetCompanyRatios(AbstractAction):
    @staticmethod
    def company_ratios_to_grpc(payload: dict) -> CompanyRatios:
        company_ratios = CompanyRatios()
        json_format.ParseDict(
            js_dict={"values": payload["data"]},
            message=company_ratios,
            ignore_unknown_fields=False,
            descriptor_pool=None,
        )
        return company_ratios

    @classmethod
    def get_company_ratios(
        cls,
        product_isin: str,
        session_id: str,
        credentials: Credentials,
        raw: bool = False,
        session: requests.Session | None = None,
        logger: logging.Logger | None = None,
    ) -> Union[CompanyRatios, dict, None]:
        if logger is None:
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        int_account = credentials.int_account
        url = f"{urls.COMPANY_RATIOS}/{product_isin}"

        params = {
            "intAccount": int_account,
            "sessionId": session_id,
        }

        request = requests.Request(method="GET", url=url, params=params)
        prepped = session.prepare_request(request)
        prepped.headers["cookie"] = "JSESSIONID=" + session_id

        response_raw = None

        try:
            response_raw = session.send(prepped)
            response_raw.raise_for_status()
            response_dict = response_raw.json()

            if raw is True:
                return response_dict
            else:
                return cls.company_ratios_to_grpc(
                    payload=response_dict,
                )
        except Exception as e:
            logger.fatal("error")
            logger.fatal(response_raw)
            logger.fatal(e)
            return None

    def call(
        self,
        product_isin: str,
        raw: bool = False,
    ) -> Union[CompanyRatios, dict, None]:
        connection_storage = self.connection_storage
        session_id = connection_storage.session_id
        session = self.session_storage.session
        credentials = self.credentials
        logger = self.logger

        return self.get_company_ratios(
            product_isin=product_isin,
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )
