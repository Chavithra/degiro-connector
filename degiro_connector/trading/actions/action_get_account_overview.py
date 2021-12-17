# IMPORTATION STANDARD
import datetime
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
    AccountOverview,
)


class ActionGetAccountOverview(AbstractAction):
    @staticmethod
    def account_overview_to_grpc(payload: dict) -> AccountOverview:
        account_overview = AccountOverview()
        account_overview.response_datetime.GetCurrentTime()
        json_format.ParseDict(
            js_dict={"values": payload["data"]},
            message=account_overview,
            ignore_unknown_fields=True,
            descriptor_pool=None,
        )

        return account_overview

    @staticmethod
    def account_overview_request_to_api(
        request: AccountOverview.Request,
    ) -> dict:
        request_dict = dict()
        request_dict["fromDate"] = datetime.datetime(
            year=request.from_date.year,
            month=request.from_date.month,
            day=request.from_date.day,
        ).strftime("%d/%m/%Y")
        request_dict["toDate"] = datetime.datetime(
            year=request.to_date.year,
            month=request.to_date.month,
            day=request.to_date.day,
        ).strftime("%d/%m/%Y")

        return request_dict

    @classmethod
    def get_account_overview(
        cls,
        request: AccountOverview.Request,
        session_id: str,
        credentials: Credentials,
        raw: bool = False,
        session: requests.Session = None,
        logger: logging.Logger = None,
    ) -> Union[AccountOverview, Dict, None]:
        """Retrieve information about the account.
        Args:
            request (AccountOverview.Request):
                List of options that we want to retrieve from the endpoint.
                Example :
                    from_date = AccountOverview.Request.Date(
                        year=2020,
                        month=10,
                        day=15,
                    )
                    from_date = AccountOverview.Request.Date(
                        year=2020,
                        month=10,
                        day=16,
                    )
                    request = AccountOverview.Request(
                        from_date=from_date,
                        to_date=to_date,
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
            AccountOverview: API response.
        """

        if logger is None:
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        url = urls.ACCOUNT_OVERVIEW
        params = cls.account_overview_request_to_api(
            request=request,
        )
        params["intAccount"] = credentials.int_account
        params["sessionId"] = session_id

        http_request = requests.Request(method="GET", url=url, params=params)
        prepped = session.prepare_request(http_request)
        response_raw = None

        try:
            response_raw = session.send(prepped, verify=False)
            response_raw.raise_for_status()
            response_dict = response_raw.json()

            if raw is True:
                return response_dict
            else:
                return cls.account_overview_to_grpc(
                    payload=response_dict,
                )
        except requests.HTTPError as e:
            status_code = getattr(response_raw, "status_code", "No status_code found.")
            text = getattr(response_raw, "text", "No text found.")
            logger.fatal(status_code)
            logger.fatal(text)
            return None
        except Exception as e:
            logger.fatal(e)
            return None

    def call(
        self,
        request: AccountOverview.Request,
        raw: bool = False,
    ) -> Union[AccountOverview, Dict, None]:
        connection_storage = self.connection_storage
        session_id = connection_storage.session_id
        session = self.session_storage.session
        credentials = self.credentials
        logger = self.logger

        return self.get_account_overview(
            request=request,
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )
