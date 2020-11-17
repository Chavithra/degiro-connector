import quotecast.helpers.pb_handler as pb_handler

from quotecast.pb.quotecast_pb2 import Ticker

class MetricsStorage:
    def __init__(self):
        self.__storage_ticker = Ticker()
    
    def __add_metrics(self, ticker:Ticker):
        storage_ticker = self.__storage_ticker
        pb_handler.merge_tickers(
            ticker1=storage_ticker,
            ticker2=ticker,
            update_only=False,
        )
    
    def fill_ticker(self, ticker:Ticker):
        storage_ticker = self.__storage_ticker

        self.__add_metrics(ticker=ticker)
            
        pb_handler.merge_tickers(
            ticker1=ticker,
            ticker2=storage_ticker,
            update_only=True,
        )