# IMPORTATION STANDARD
from typing import Dict, List, Union

# IMPORTATION THIRD PARTY
# IMPORTATION INTERNAL
from degiro_connector.quotecast.models.quotecast_pb2 import Ticker


class MetricsStorage:
    @staticmethod
    def merge_tickers(
        ticker1: Ticker,
        ticker2: Ticker,
        update_only: bool = False,
    ):
        """Override metrics of ticker1 with ticker2's metrics.
        Args:
            ticker1 (Ticker): Ticker to fill.
            ticker2 (Ticker): Ticker used to fill.
            update_only (bool, optional):
                Whether or not we want to add products from "ticker2" to
                "ticker1".
        """

        if update_only is True:
            for ticker2_product in ticker2.products:
                if ticker2_product in ticker1.products:
                    ticker1.products[ticker2_product].metrics.update(
                        ticker2.products[ticker2_product].metrics
                    )
        else:
            for ticker2_product in ticker2.products:
                ticker1.products[ticker2_product].metrics.update(
                    ticker2.products[ticker2_product].metrics
                )

    @property
    def storage_ticker(self) -> Ticker:
        return self.__storage_ticker

    def __init__(self):
        self.__storage_ticker = Ticker()

    def add_metrics(self, ticker: Ticker):
        storage_ticker = self.__storage_ticker
        self.merge_tickers(
            ticker1=storage_ticker,
            ticker2=ticker,
            update_only=False,
        )

    def fill_ticker(self, ticker: Ticker):
        storage_ticker = self.__storage_ticker

        self.add_metrics(ticker=ticker)

        self.merge_tickers(
            ticker1=ticker,
            ticker2=storage_ticker,
            update_only=True,
        )
