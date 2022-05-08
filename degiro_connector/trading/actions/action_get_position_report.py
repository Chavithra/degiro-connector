# IMPORTATION STANDARD
import datetime
import logging
from typing import Union

# IMPORTATION THIRD PARTY
import requests

# IMPORTATION INTERNAL
from degiro_connector.core.constants import urls
from degiro_connector.core.abstracts.abstract_action import AbstractAction
from degiro_connector.trading.models.trading_pb2 import (
    Credentials,
    PositionReport,
)


class ActionGetPositionReport(AbstractAction):
    @staticmethod
    def position_report_request_to_api(
        request: PositionReport.Request,
    ) -> dict:
        request_dict = dict()
        request_dict["country"] = request.country
        request_dict["lang"] = request.lang
        request_dict["toDate"] = datetime.datetime(
            year=request.to_date.year,
            month=request.to_date.month,
            day=request.to_date.day,
        ).strftime("%d/%m/%Y")

        return request_dict

    @staticmethod
    def position_report_to_grpc(
        request: PositionReport.Request,
        payload: str,
    ) -> PositionReport:
        position_report = PositionReport()
        position_report.response_datetime.GetCurrentTime()
        position_report.content = payload
        position_report.format = request.format

        return position_report

    @classmethod
    def get_position_report(
        cls,
        request: PositionReport.Request,
        session_id: str,
        credentials: Credentials,
        raw: bool = False,
        session: requests.Session = None,
        logger: logging.Logger = None,
    ) -> Union[PositionReport, str, None]:
        """Retrieve information about the account in a specific format.
        Args:
            request (PositionReport.Request):
                List of options that we want to retrieve from the endpoint.
                Example :
                    to_date = PositionReport.Request.Date(
                        year=2020,
                        month=10,
                        day=15,
                    )
                    request = PositionReport.Request(
                        format=PositionReport.Format.CSV,
                        country='FR',
                        lang='fr',
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
            PositionReport: API response.
        """

        if logger is None:
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        format = PositionReport.Format.Name(request.format)
        url = f"{urls.POSITION_REPORT}/{format}"
        params = cls.position_report_request_to_api(
            request=request,
        )
        params["intAccount"] = credentials.int_account
        params["sessionId"] = session_id

        req = requests.Request(method="GET", url=url, params=params)
        prepped = session.prepare_request(req)
        response_raw = None

        try:
            response_raw = session.send(prepped)
            response_raw.raise_for_status()
            response_text = response_raw.text

            if raw is True:
                return response_text
            else:
                return cls.position_report_to_grpc(
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
        request: PositionReport.Request,
        raw: bool = False,
    ) -> Union[PositionReport, str, None]:
        connection_storage = self.connection_storage
        session_id = connection_storage.session_id
        session = self.session_storage.session
        credentials = self.credentials
        logger = self.logger

        return self.get_position_report(
            request=request,
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )
