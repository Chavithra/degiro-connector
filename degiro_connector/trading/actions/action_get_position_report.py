import logging

import requests

from degiro_connector.core.constants import urls
from degiro_connector.core.abstracts.abstract_action import AbstractAction
from degiro_connector.trading.models.credentials import Credentials
from degiro_connector.trading.models.account import Report, ReportRequest


class ActionGetPositionReport(AbstractAction):
    @staticmethod
    def build_model(
        report_request: ReportRequest, response: requests.Response
    ) -> Report:
        model = Report(
            content=response.text,
            format=report_request.format,
        )

        return model

    @staticmethod
    def build_params_map(report_request: ReportRequest) -> dict:
        params_map = report_request.model_dump(
            by_alias=True,
            exclude={"format"},
            exclude_none=True,
            mode="json",
        )

        return params_map

    @classmethod
    def get_position_report(
        cls,
        report_request: ReportRequest,
        session_id: str,
        credentials: Credentials,
        raw: bool = False,
        session: requests.Session | None = None,
        logger: logging.Logger | None = None,
    ) -> Report | str | None:
        """Retrieve information about the account in a specific format.
        Args:
            request (ReportRequest):
                list of options that we want to retrieve from the endpoint.
                Example :
                    report_request = OverviewRequest(
                        from_date=date(year=2023, month=10, day=15),
                        to_date=date(year=2024, month=1, day=1),
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
            Report: API response.
        """

        if logger is None:
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        int_account = credentials.int_account
        url = f"{urls.POSITION_REPORT}/{report_request.format.value}"
        params_map = cls.build_params_map(report_request=report_request)
        params_map.update({"intAccount": int_account, "sessionId": session_id})

        request = requests.Request(method="GET", url=url, params=params_map)
        prepped = session.prepare_request(request=request)

        try:
            response = session.send(prepped)
            response.raise_for_status()

            if raw is True:
                model = response.text
            else:
                model = cls.build_model(
                    report_request=report_request,
                    response=response,
                )
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
        report_request: ReportRequest,
        raw: bool = False,
    ) -> Report | str | None:
        connection_storage = self.connection_storage
        session_id = connection_storage.session_id
        session = self.session_storage.session
        credentials = self.credentials
        logger = self.logger

        return self.get_position_report(
            report_request=report_request,
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )
