import degiro_connector.quotecast.helpers.pb_handler as pb_handler

from degiro_connector.quotecast.pb.quotecast_pb2 import Ticker


class MetricsStorage:
    @property
    def storage_ticker(self) -> Ticker:
        return self.__storage_ticker

    def __init__(self):
        self.__storage_ticker = Ticker()

    def add_metrics(self, ticker: Ticker):
        storage_ticker = self.__storage_ticker
        pb_handler.merge_tickers(
            ticker1=storage_ticker,
            ticker2=ticker,
            update_only=False,
        )

    def fill_ticker(self, ticker: Ticker):
        storage_ticker = self.__storage_ticker

        self.add_metrics(ticker=ticker)

        pb_handler.merge_tickers(
            ticker1=ticker,
            ticker2=storage_ticker,
            update_only=True,
        )
