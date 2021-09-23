# IMPORTATION STANDARD
import requests
import logging
from typing import Dict

# IMPORTATION THIRD PARTY
import orjson as json
from google.protobuf import json_format

# IMPORTATION INTERNAL
import degiro_connector.core.constants.urls as urls
from degiro_connector.quotecast.models.quotecast_pb2 import (
    Chart,
    Quotecast,
)
from degiro_connector.core.abstracts.abstract_action import AbstractAction


class ActionGetChart(AbstractAction):
    @staticmethod
    def chart_request_to_api(request: Chart.Request) -> dict:
        request_dict = json_format.MessageToDict(
            message=request,
            including_default_value_fields=True,
            preserving_proto_field_name=False,
            use_integers_for_enums=False,
            descriptor_pool=None,
            float_precision=None,
        )

        return request_dict

    @staticmethod
    def api_to_chart(payload: dict) -> Chart:
        chart = Chart()
        json_format.ParseDict(
            js_dict=payload,
            message=chart,
            ignore_unknown_fields=True,
            descriptor_pool=None,
        )

        return chart

    @classmethod
    def get_chart(
        cls,
        request: Chart.Request,
        user_token: int,
        logger: logging.Logger = None,
        override: Dict[str, str] = None,
        raw: bool = False,
        session: requests.Session = None,
    ) -> Chart:
        """Fetches chart's data.
        Args:
            request (Chart.Request):
                Example :
                    request = Chart.Request()
                    request.requestid = '1'
                    request.resolution = Chart.Interval.PT1M
                    request.culture = 'fr-FR'
                    request.series.append('issueid:360148977')
                    request.series.append('price:issueid:360148977')
                    request.series.append('ohlc:issueid:360148977')
                    request.series.append('volume:issueid:360148977')
                    request.period = Chart.Interval.P1D
                    request.tz = 'Europe/Paris'
            user_token (int):
                User identifier in Degiro's API.
            override (Dict[str], optional):
                Overrides the request sent to Degiro's API.
                Example :
                    override = {
                        'period':'P6D',
                    }
                Defaults to None.
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
            Chart: Data of the chart.
        """

        if logger is None:
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        url = urls.CHART
        params = cls.chart_request_to_api(request=request)
        params["format"] = "json"
        params["callback"] = ""
        params["userToken"] = user_token

        if override is not None:
            for key, value in override.items():
                params[key] = value

        request = requests.Request(method="GET", url=url, params=params)
        prepped = session.prepare_request(request)
        response_raw = None

        try:
            response_raw = session.send(prepped, verify=False)
            response_dict = json.loads(response_raw.text)

            if raw is True:
                response = response_dict
            else:
                response = cls.api_to_chart(payload=response_dict)

        except Exception as e:
            logger.fatal(response_raw.status_code)
            logger.fatal(response_raw.text)
            logger.fatal(e)
            return False

        return response

    def call(
        self,
        request: Quotecast.Request,
        override: Dict[str, str] = None,
        raw: bool = False,
    ):
        session = self.session_storage.session
        logger = self.logger
        credentials = self.credentials
        user_token = credentials["user_token"]

        return self.get_chart(
            request=request,
            user_token=user_token,
            logger=logger,
            override=override,
            raw=raw,
            session=session,
        )
