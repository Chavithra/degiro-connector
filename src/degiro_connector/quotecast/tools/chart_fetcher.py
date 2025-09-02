import logging
from datetime import datetime, timedelta
from typing import Any

import json
import polars as pl
import requests
from isodate import parse_duration

from degiro_connector.core.constants import urls
from degiro_connector.quotecast.models.chart import Chart, ChartRequest, Series
from degiro_connector.core.models.model_connection import ModelConnection
from degiro_connector.core.models.model_session import ModelSession


class SeriesFormatter:
    @staticmethod
    def is_timeseries(series: Series) -> bool:
        return series.type in ["time", "ohlc"]

    @staticmethod
    def parse_date_and_resolution(times: str) -> tuple[datetime, timedelta]:
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
            tuple[datetime, timedelta]:
                Start datetime and resolution.
        """
        start, resolution = times.split(sep="/", maxsplit=1)
        start_datetime = datetime.fromisoformat(start)
        resolution_interval = parse_duration(resolution)

        return start_datetime, resolution_interval

    @staticmethod
    def format_timestamp(
        df: pl.DataFrame,
        column: str,
        start: datetime,
        resolution: timedelta,
    ):
        df = df.with_columns((pl.col(column) * resolution).cast(pl.Duration) + start)

        return df

    @classmethod
    def format(
        cls,
        series: Series,
        columns: list[str] | None = None,
    ) -> pl.DataFrame:
        if series.type is None:
            raise TypeError("Can't parse `None` series.")

        if not cls.is_timeseries(series=series):
            raise TypeError(f"Only timeseries can be formatted, type={series.type}")

        if series.times is None or series.type not in ["time", "ohlc"]:
            raise AttributeError("The attributes `times` is empty.")

        if columns:
            pass
        elif series.id.startswith("price"):
            columns = ["timestamp", "price"]
        elif series.id.startswith("volume"):
            columns = ["timestamp", "volume"]
        elif series.id.startswith("ohlc"):
            columns = ["timestamp", "open", "high", "low", "close"]
        else:
            columns = None

        df = pl.DataFrame(
            data=series.data,
            orient="row",
            schema=columns,
        )
        start, resolution = cls.parse_date_and_resolution(times=series.times)
        column = df.columns[0]
        formatted_df = cls.format_timestamp(
            df=df, column=column, start=start, resolution=resolution
        )

        return formatted_df

    @classmethod
    def format_series(
        cls,
        series: Series,
        columns: list[str] | None = None,
    ) -> pl.DataFrame:
        if cls.is_timeseries(series=series):
            df = cls.format(
                series=series,
                columns=columns,
            )
        else:
            df = pl.DataFrame(series.data)

        return df


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
            response_map = json.loads(
                response.text[len(chart_request.callback) + 1 : -1]
            )

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
