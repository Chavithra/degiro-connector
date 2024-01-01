import logging
from datetime import datetime
from typing import Any

import json
import pandas as pd
import requests
from google.protobuf import json_format
from google.protobuf.message import Message

from degiro_connector.core.constants import urls
from degiro_connector.quotecast.models.chart import Chart, ChartRequest, Series
from degiro_connector.core.models.model_connection import ModelConnection
from degiro_connector.core.models.model_session import ModelSession


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

        # with "PT1M":
        # {'requestid': '', 'start': '2023-06-30T00:00:00+02:00', 'end': '2023-06-30T21:59:59+02:00', 'resolution': 'PT1M', 'series': [{'times': '2023-06-30/PT1M', 'expires': '2023-07-02T14:10:43.1908462+02:00', 'data':
        # error when doing : ChartHelper.format_chart(chart=chart, copy=False) :
        # time data '2023-06-30' does not match format '%Y-%m-%dT%H:%M:%S'
        # same with "PT5M"
        # {'requestid': '', 'start': '2023-06-30T00:00:00+02:00', 'end': '2023-06-30T21:59:59+02:00', 'resolution': 'PT5M', 'series': [{'times': '2023-06-30/PT5M', 'expires': '2023-07-02T14:17:36.4487987+02:00', 'data':
        # same with "PT{xxx}" ...
        # conclusion : it's always --> date_format = "%Y-%m-%d"

        """
        previous code:
        if resolution.startswith("PT"):
            date_format = "%Y-%m-%dT%H:%M:%S"
        else:
            date_format = "%Y-%m-%d"
        """

        # new code :
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
    def format_serie(cls, serie: Series, copy: bool = True) -> Series:
        """By default a time serie uses the order as index.
        This method convert the indexes into `timestamp in seconds`.
        Args:
            serie (Series):
                Serie to format.
            copy (bool, optional):
                Whether or not to make a copy before the formatting.
                Defaults to True.

        Returns:
            Series: [description]
        """
        if copy:
            serie = serie.model_copy()

        if serie.type in ["time"]:
            times = serie.times
            if times:
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
            chart = chart.model_copy()

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
    def serie_to_df(cls, serie: Series) -> pd.DataFrame:
        """Converts a timeserie into a DataFrame.
        Only series with the following types can be converted into DataFrame :
        - serie.type == "time"
        - serie.type == "ohlc"
        Beware of series with the following type :
         - serie.type == "object"
        These are not actual timeseries and can't converted into DataFrame.
        Args:
            serie (Series):
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


class ChartFetcher:
    @staticmethod
    def build_logger() -> logging.Logger:
        return logging.getLogger(__name__)

    @staticmethod
    def build_session(headers: dict[str, str] | None = None) -> requests.Session:
        return ModelSession.build_session(headers=headers)

    @property
    def user_token(self):
        return self.__user_token

    @property
    def connection_storage(self):
        return self.__connection_storage

    @property
    def logger(self):
        return self.__logger

    @property
    def session_storage(self):
        return self._session_storage

    @staticmethod
    def build_params(
        chart_request: ChartRequest,
        user_token: int,
    ) -> dict[str, Any]:
        chart_request.user_token = chart_request.user_token or user_token
        params = chart_request.model_dump(
            by_alias=True,
            exclude={"override"},
            exclude_none=True,
            mode="json",
        )
        params.update(chart_request.override)

        return params

    def get_chart(
        self,
        chart_request: ChartRequest,
        logger: logging.Logger | None = None,
        raw: bool = False,
        session: requests.Session | None = None,
    ) -> Chart | None:
        """Fetches chart's data.
        Args:
            request (ChartRequest):
                Example :
                    chart_request = ChartRequest(
                        culture = "fr-FR",
                        # override={
                        #     "resolution": "P1D",
                        #     "period": "P1W",
                        # },
                        period = Interval.P1D,
                        requestid = "1",
                        resolution = Interval.PT1H,
                        series=[
                            "issueid:360148977",
                            # "price:issueid:360148977",
                            # "ohlc:issueid:360148977",
                            # "volume:issueid:360148977",
                            # "vwdkey:AAPL.BATS,E",
                            # "price:vwdkey:AAPL.BATS,E",
                            # "ohlc:vwdkey:AAPL.BATS,E",
                            # "volume:vwdkey:AAPL.BATS,E",
                        ],
                        tz = "Europe/Paris",
                    )

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

        session = self.session_storage.session
        logger = self.logger
        user_token = self.__user_token

        if logger is None:
            logger = self.build_logger()
        if session is None:
            session = self.build_session()

        url = urls.CHART
        params = self.build_params(
            chart_request=chart_request,
            user_token=user_token,
        )

        http_request = requests.Request(method="GET", url=url, params=params)
        prepped = session.prepare_request(http_request)

        try:
            response = session.send(prepped)
            response.raise_for_status()
            response_map = json.loads(response.text[len(chart_request.callback) + 1 : -1])

            if raw is True:
                chart = response_map
            else:
                chart = Chart.model_validate(obj=response_map)

            return chart
        except requests.HTTPError as e:
            logger.fatal(e)
            if isinstance(e.response, requests.Response):
                logger.fatal(e.response.text)
            return None
        except Exception as e:
            logger.fatal(e)
            return None

    def __init__(
        self,
        user_token: int,
        connection_storage: ModelConnection | None = None,
        logger: logging.Logger | None = None,
        session_storage: ModelSession | None = None,
    ):
        self.__user_token = user_token
        self.__connection_storage = connection_storage or ModelConnection(timeout=600)
        self.__logger = logger or logging.getLogger(self.__module__)
        self._session_storage = session_storage or ModelSession(
            hooks=self.__connection_storage.build_hooks(),
        )
