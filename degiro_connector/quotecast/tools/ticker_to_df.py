from copy import deepcopy

import polars as pl

from degiro_connector.quotecast.models.metric import Metric
from degiro_connector.quotecast.models.ticker import Ticker
from degiro_connector.quotecast.tools.ticker_to_metric_list import TickerToMetricList


class TickerToDF:
    @staticmethod
    def merge_metric_list(
        current_data: list[Metric],
        new_data: list[Metric],
    ) -> list[Metric]:
        current_data = deepcopy(current_data)
        metric_map = {
            f"{metric.product_id} {metric.metric_type.value}": metric
            for metric in current_data
        }

        for new_metric in new_data:
            map_key = f"{new_metric.product_id} {new_metric.metric_type.value}"
            metric_map[map_key] = new_metric

        return list(metric_map.values())

    @staticmethod
    def build_df(metric_list: list[Metric]) -> pl.DataFrame:
        df = pl.DataFrame(
            data=[metric.model_dump() for metric in metric_list],
            schema={
                "product_id": pl.Utf8,
                "metric_type": pl.Utf8,
                "value": pl.Utf8,
            },
        )

        df = df.pivot(index="product_id", columns="metric_type", values="value")

        # PRICE
        price_column_list = list(
            filter(lambda column: column.endswith("Price"), df.columns)
        )
        df = df.with_columns(
            pl.col(column).cast(pl.Float64) for column in price_column_list
        )

        # VOLUME
        volume_column_list = list(
            filter(lambda column: column.endswith("Volume"), df.columns)
        )
        df = df.with_columns(
            pl.col(column).cast(pl.Int64) for column in volume_column_list
        )

        # ORDERS
        order_column_list = list(
            filter(lambda column: column.endswith("Orders"), df.columns)
        )
        df = df.with_columns(
            pl.col(column).cast(pl.Int64) for column in order_column_list
        )

        # LASTDATETIMEUTC
        if "LastDate" in df.columns:
            if "LastTime" not in df.columns:
                df = df.with_columns((pl.lit("00:00:00")).alias("LastTime"))

            df = df.with_columns(
                (pl.col("LastDate") + " " + pl.col("LastTime")).alias("LastDatetime")
            )
            df = df.drop(["LastDate", "LastTime"])
            df = df.with_columns(
                pl.col("LastDatetime")
                .str.strptime(pl.Datetime, format="%Y-%m-%d %H:%M:%S")
                .alias("LastDatetime")
            )
            df = df.with_columns(
                pl.col("LastDatetime").dt.replace_time_zone("Europe/Paris")
            )

            df_utc = df.with_columns(
                pl.col("LastDatetime").dt.convert_time_zone("UTC").alias("LastDatetimeUTC")
            )
            df_utc = df_utc.with_columns(
                pl.col("LastDatetimeUTC").dt.replace_time_zone(None)
            )
            df_utc = df_utc.drop("LastDatetime")
            df = df_utc

        return df

    def __init__(self) -> None:
        self.__last_df = None
        self.__last_metric_list = []
        self.__stored_request_duration_map = {}
        self.__stored_response_datetime_map = {}
        self.__stored_metric_list = []
        self.__ticker_to_metric_list = TickerToMetricList()

    @property
    def last_df(self) -> pl.DataFrame | None:
        return self.__last_df

    @property
    def last_metric_list(self) -> list[Metric]:
        return self.__last_metric_list

    @property
    def stored_metric_list(self) -> list[Metric]:
        return self.__stored_metric_list

    @property
    def ticker_to_metric_list(self) -> TickerToMetricList:
        return self.__ticker_to_metric_list

    def add_request_duration_column(
        self,
        df: pl.DataFrame,
        last_metric_list: list[Metric],
        ticker: Ticker,
    ) -> pl.DataFrame:
        request_duration_map = {
            metric.product_id: ticker.request_duration.total_seconds()
            for metric in last_metric_list
        }
        self.__stored_request_duration_map.update(request_duration_map)

        df = df.with_columns(
            request_duration_s=pl.col("product_id")
            .map_elements(lambda x: self.__stored_request_duration_map.get(x, None),
                          return_dtype=pl.Int64)
            .cast(pl.Int64)
        )

        return df

    def add_response_datetime_column(
        self,
        df: pl.DataFrame,
        last_metric_list: list[Metric],
        ticker: Ticker,
    ) -> pl.DataFrame:
        response_datetime = {
            metric.product_id: ticker.response_datetime for metric in last_metric_list
        }
        self.__stored_response_datetime_map.update(response_datetime)

        df = df.with_columns(
            response_datetime=pl.col("product_id").map_elements(
                lambda x: self.__stored_response_datetime_map.get(x, None),
                return_dtype=pl.Datetime
            )
        )
        df = df.with_columns(
            pl.col("response_datetime").dt.replace_time_zone("Europe/Paris")
        )

        df = df.with_columns(
            pl.col("response_datetime")
            .dt.convert_time_zone("UTC")
            .alias("response_datetime_utc")
        )
        df = df.with_columns(pl.col("response_datetime_utc").dt.replace_time_zone(None))
        df = df.drop("response_datetime")

        return df

    def parse(self, ticker: Ticker) -> pl.DataFrame | None:
        stored_metric_list = self.__stored_metric_list
        ticker_to_metric_list = self.__ticker_to_metric_list

        if ticker.json_text != '[{"m":"h"}]':
            last_metric_list = ticker_to_metric_list.parse(ticker=ticker)
            stored_metric_list = self.merge_metric_list(
                current_data=stored_metric_list,
                new_data=last_metric_list,
            )

            df = self.build_df(metric_list=stored_metric_list)
            df = self.add_request_duration_column(
                df=df,
                last_metric_list=last_metric_list,
                ticker=ticker,
            )
            df = self.add_response_datetime_column(
                df=df,
                last_metric_list=last_metric_list,
                ticker=ticker,
            )
        else:
            last_metric_list = []
            df = None

        self.__last_df = df
        self.__last_metric_list = last_metric_list
        self.__stored_metric_list = stored_metric_list

        return df
