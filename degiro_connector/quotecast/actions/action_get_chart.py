# IMPORTATION STANDARD
import logging
from datetime import datetime
from typing import Optional

# IMPORTATION THIRD PARTY
import json
import pandas as pd
import requests
from google.protobuf import json_format
from google.protobuf.message import Message

# IMPORTATION INTERNAL
import degiro_connector.core.constants.urls as urls
from degiro_connector.quotecast.models.quotecast_pb2 import (
    Chart,
)
from degiro_connector.core.abstracts.abstract_action import AbstractAction


class ChartHelper:
    UNITS_MATCHING = {
        "PT1S": 1,
        "PT1M": 60,
        "PT1H": 3600,
        "P1D": 3600 * 24,
        "P1W": 3600 * 24 * 7,
        "P1M": 3600 * 24 * 30,
        "P1Y": 3600 * 24 * 365,  # Year resolution doesn't seem to be supported
    }

    @staticmethod
    def parse_start_timestamp(times: str) -> float:
        """Extract the start timestamp of a timeserie.
        Args:
            times (str):
                Combination of `start date` and `resolution` of the serie.
                Example :
                    times = "2021-10-28/P6M"
                    times = "2021-11-03T00:00:00/PT1H"
        Returns:
            float:
                Timestamp of the start date of the serie.
        """

        (start, resolution) = times.rsplit(sep="/", maxsplit=1)

        date_format = ""
        if resolution.startswith("PT"):
            date_format = "%Y-%m-%dT%H:%M:%S"
        else:
            date_format = "%Y-%m-%d"

        start_datetime = datetime.strptime(start, date_format)
        start_timestamp = start_datetime.timestamp()

        return start_timestamp

    @classmethod
    def parse_interval_in_seconds(cls, times: str) -> int:
        """Extract the interval of a timeserie.
        Args:
            times (str):
                Combination of `start date` and `resolution` of the serie.
                Example :
                    times = "2021-10-28/P6M"
                    times = "2021-11-03T00:00:00/PT1H"
        Raises:
            AttributeError:
                if the resolution is unknown.
        Returns:
            int:
                Number of seconds in the interval.
        """
        (_start, resolution) = times.rsplit(sep="/", maxsplit=1)

        prefix = ""
        if resolution.startswith("PT"):
            prefix = "PT"
        elif resolution.startswith("P"):
            prefix = "P"
        else:
            raise AttributeError("Unkown resolution")

        unit = prefix + "1" + resolution[-1]
        number = int(resolution[len(prefix) : -1])

        interval = cls.UNITS_MATCHING[unit] * int(number)

        return interval

    @classmethod
    def format_serie(cls, serie: Chart.Serie, copy: bool = True) -> Chart.Serie:
        """By default a time serie uses the order as index.
        This method convert the indexes into `timestamp in seconds`.
        Args:
            serie (Chart.Serie):
                Serie to format.
            copy (bool, optional):
                Whether or not to make a copy before the formatting.
                Defaults to True.

        Returns:
            Chart.Serie: [description]
        """
        if copy:
            serie_copy = Chart.Serie()
            serie_copy.CopyFrom(serie)
            serie = serie_copy

        if serie.type in ["time", "ohlc"]:
            times = serie.times
            start = cls.parse_start_timestamp(times=times)
            interval = cls.parse_interval_in_seconds(times=times)

            for datapoint in serie.data:
                datapoint[0] = start + datapoint[0] * interval

        return serie

    @classmethod
    def format_chart(cls, chart: Chart, copy: bool = True) -> Chart:
        """By default a time serie uses the order as index.
        This method convert series`s indexes into `timestamp in seconds`.
        Args:
            chart (Chart):
                Chart containing the series.
            copy (bool, optional):
                Whether or not to make a copy before the formatting.
                Defaults to True.
        Returns:
            Chart:
                Formatted Chart.
        """

        if copy:
            chart_copy = Chart()
            chart_copy.CopyFrom(chart)
            chart = chart_copy

        for serie in chart.series:
            cls.format_serie(serie=serie, copy=False)

        return chart

    @staticmethod
    def message_to_dict(message: Message) -> dict:
        return json_format.MessageToDict(
            message=message,
            including_default_value_fields=True,
            preserving_proto_field_name=True,
            use_integers_for_enums=True,
            descriptor_pool=None,
            float_precision=None,
        )

    @classmethod
    def serie_to_df(cls, serie: Chart.Serie) -> pd.DataFrame:
        """Converts a timeserie into a DataFrame.
        Only series with the following types can be converted into DataFrame :
        - serie.type == "time"
        - serie.type == "ohlc"
        Beware of series with the following type :
         - serie.type == "object"
        These are not actual timeseries and can't converted into DataFrame.
        Args:
            serie (Chart.Serie):
                The serie to convert.
        Raises:
            AttributeError:
                If the serie.type is incorrect.
        Returns:
            pd.DataFrame: [description]
        """
        columns = []
        if serie.type == "ohlc" and serie.id.startswith("ohlc:"):
            columns = [
                "timestamp",
                "open",
                "high",
                "low",
                "close",
            ]
        elif serie.type == "time" and serie.id.startswith("price:"):
            columns = [
                "timestamp",
                "price",
            ]
        elif serie.type == "time" and serie.id.startswith("volume:"):
            columns = [
                "timestamp",
                "volume",
            ]
        elif serie.type == "object":
            raise AttributeError(f"Not a timeserie, serie.type = {serie.type}")
        else:
            raise AttributeError(f"Unknown serie, serie.type = {serie.type}")

        return pd.DataFrame.from_records(serie.data, columns=columns)


class ActionGetChart(AbstractAction):
    CALLBACK = "vwd.hchart.seriesRequestManager.sync_response"

    @staticmethod
    def chart_request_to_api(
        request: Chart.Request,
        user_token: int,
    ) -> dict:
        request_dict = json_format.MessageToDict(
            message=request,
            including_default_value_fields=True,
            preserving_proto_field_name=False,
            use_integers_for_enums=False,
            descriptor_pool=None,
            float_precision=None,
        )
        request_dict["format"] = "json"
        request_dict["callback"] = "vwd.hchart.seriesRequestManager.sync_response"
        request_dict["userToken"] = user_token

        for key, value in request.override.items():
            request_dict[key] = value

        return request_dict

    @staticmethod
    def api_to_chart(payload: dict) -> Chart:
        for serie in payload["series"]:
            if serie["type"] == "object":
                serie["data"] = [serie["data"]]

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
        raw: bool = False,
        session: requests.Session = None,
    ) -> Optional[Chart]:
        """Fetches chart's data.
        Args:
            request (Chart.Request):
                Example :
                    request = Chart.Request()
                    request.culture = "fr-FR"
                    request.period = Chart.Interval.PT1H
                    request.requestid = "1"
                    request.resolution = Chart.Interval.P1D
                    # request.series.append("issueid:360148977")
                    request.series.append("price:issueid:360148977")
                    # request.series.append("ohlc:issueid:360148977")
                    # request.series.append("volume:issueid:360148977")
                    # request.series.append("vwdkey:AAPL.BATS,E")
                    # request.series.append("price:vwdkey:AAPL.BATS,E")
                    # request.series.append("ohlc:vwdkey:AAPL.BATS,E")
                    # request.series.append("volume:vwdkey:AAPL.BATS,E")
                    request.tz = "Europe/Paris"
                    request.override["resolution"] = "P1D"
                    request.override["period"] = "P1W"

                    The parameter `request.override` allows overriding
                    the request sent to Degiro's API.
            user_token (int):
                User identifier in Degiro's API.
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
        params = cls.chart_request_to_api(
            request=request,
            user_token=user_token,
        )

        http_request = requests.Request(method="GET", url=url, params=params)
        prepped = session.prepare_request(http_request)
        response_raw = None

        try:
            response_raw = session.send(prepped, verify=False)
            response_raw.raise_for_status()
            response_dict = json.loads(response_raw.text[len(cls.CALLBACK) + 1 : -1])

            if raw is True:
                return response_dict
            else:
                return cls.api_to_chart(payload=response_dict)

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
        request: Chart.Request,
        raw: bool = False,
    ) -> Optional[Chart]:
        session = self.session_storage.session
        logger = self.logger
        credentials = self.credentials
        user_token = credentials["user_token"]

        return self.get_chart(
            request=request,
            user_token=user_token,
            logger=logger,
            raw=raw,
            session=session,
        )
