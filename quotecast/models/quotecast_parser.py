import logging

from quotecast.models.metric_list_storage import MetricListSorage
from quotecast.models.raw_metric_parser import RawMetricParser
from quotecast.pb.quotecast_pb2 import (
    Quotecast,
    Ticker,
)
from typing import List
from wrapt.decorators import synchronized

class QuotecastParser:
    """ Parse Quotecast retrieved from Degiro's API.
    It build Ticker object from it.
    """

    @staticmethod
    def extract_product_list(
        metric_list,
    )->List[int]:
        metric_list = metric_list

        product_list = list()
        for metric in metric_list:
            if not metric.product_id in product_list:
                product_list.append(metric.product_id)

        return product_list

    @property
    def ticker(self)->Ticker:
        return self.__ticker

    @property
    def metric_list_storage(self)->MetricListSorage:
        return self.__metric_list_storage

    @property
    def raw_metric_parser(self)->RawMetricParser:
        return self.__raw_metric_parser

    def __init__(
        self,
        fill_na:bool=True,
    ):
        """
        Args:
            fill_na (bool, optional):
                Whether or not we want to fill the Ticker with previous
                sent metrics.
        """
    
        self.__logger = logging.getLogger(self.__module__)
        self.__fill_na = fill_na
        self.__ticker = None
        self.__metric_list_storage = MetricListSorage()
        self.__raw_metric_parser = RawMetricParser()

    def put_quotecast(
        self,
        quotecast:Quotecast,
    ):
        fill_na = self.__fill_na
        metric_list_storage = self.__metric_list_storage
        raw_metric_parser = self.__raw_metric_parser

        metadata = quotecast.metadata
        json_data = quotecast.json_data

        # SETUP METRIC LIST        
        raw_metric_parser.put_raw_metric_list(raw_json=json_data)
        metric_list = raw_metric_parser.metric_list

        # SETUP PRODUCT LIST
        product_list = self.extract_product_list(
            metric_list=metric_list
        )

        # SETUP FILLED METRIC LIST
        if fill_na == True:
            metric_list_storage.put_metric_list(
                metric_list=metric_list,
            )
            filled_metric_list = metric_list_storage.get_metric_list(
                product_list=product_list,
            )
        else:
            filled_metric_list = list()

        # SETUP TICKER
        self.__ticker = Ticker(
            metric_list=metric_list,
            filled_metric_list=filled_metric_list,
            product_list=product_list,
            metadata=metadata,
        )

if __name__ == '__main__':
    data = '[{"m":"h"},{"m":"a_req","v":["360015751.LastPrice",101]},{"m":"un","v":[101,119.900000]}]'