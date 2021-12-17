# IMPORTATION STANDARD
import datetime
import logging
from typing import Union

# IMPORTATION THIRD PARTY
import requests

# IMPORTATION INTERNAL
import degiro_connector.core.constants.urls as urls
from degiro_connector.core.abstracts.abstract_action import AbstractAction
from degiro_connector.trading.models.trading_pb2 import (
    Credentials,
    CashAccountReport,
)


class ActionGetCashAccountReport(AbstractAction):
    @staticmethod
    def cash_account_report_request_to_api(
        request: CashAccountReport.Request,
    ) -> dict:
        request_dict = dict()
        request_dict["country"] = request.country
        request_dict["lang"] = request.lang
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

    @staticmethod
    def cash_account_report_to_grpc(
        request: CashAccountReport.Request,
        payload: str,
    ) -> CashAccountReport:
        cash_account_report = CashAccountReport()
        cash_account_report.response_datetime.GetCurrentTime()
        cash_account_report.content = payload
        cash_account_report.format = request.format

        return cash_account_report

    @classmethod
    def get_cash_account_report(
        cls,
        request: CashAccountReport.Request,
        session_id: str,
        credentials: Credentials,
        raw: bool = False,
        session: requests.Session = None,
        logger: logging.Logger = None,
    ) -> Union[CashAccountReport, str, None]:
        """Retrieve information about the account in a specific format.
        Args:
            request (CashAccountReport.Request):
                List of options that we want to retrieve from the endpoint.
                Example :
                    from_date = CashAccountReport.Request.Date(
                        year=2020,
                        month=10,
                        day=15,
                    )
                    from_date = CashAccountReport.Request.Date(
                        year=2020,
                        month=10,
                        day=16,
                    )
                    request = CashAccountReport.Request(
                        format=CashAccountReport.Format.CSV,
                        country='FR',
                        lang='fr',
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
            CashAccountReport: API response.
        """

        if logger is None:
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        format = CashAccountReport.Format.Name(request.format)
        url = f"{urls.CASH_ACCOUNT_REPORT}/{format}"
        params = cls.cash_account_report_request_to_api(
            request=request,
        )
        params["intAccount"] = credentials.int_account
        params["sessionId"] = session_id

        req = requests.Request(method="GET", url=url, params=params)
        prepped = session.prepare_request(req)
        response_raw = None

        try:
            response_raw = session.send(prepped, verify=False)
            response_raw.raise_for_status()
            response_text = response_raw.text

            if raw is True:
                return response_text
            else:
                return cls.cash_account_report_to_grpc(
                    request=request,
                    payload=response_text,
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
        request: CashAccountReport.Request,
        raw: bool = False,
    ) -> Union[CashAccountReport, str, None]:
        connection_storage = self.connection_storage
        session_id = connection_storage.session_id
        session = self.session_storage.session
        credentials = self.credentials
        logger = self.logger

        return self.get_cash_account_report(
            request=request,
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )
