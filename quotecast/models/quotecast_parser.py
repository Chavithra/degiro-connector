import json
import logging

import quotecast.helpers.metric_handler as metric_handler

from quotecast.models.metric_list_storage import MetricListSorage
from quotecast.pb.quotecast_pb2 import (
    Matching,
    Metadata,
    Metric,
    Quotecast,
    Ticker,
)
from typing import List
from wrapt.decorators import synchronized

class QuotecastParser:
    """ Parse Quotecast retrieved from Degiro's API.
    It build Ticker object from it.
    """

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
        self.__matching_list = None
        self.__ticker = None
        self.__metric_list_storage = MetricListSorage()

    @property
    def matching_list(self)->List[Matching]:
        return self.__matching_list

    @property
    def ticker(self)->Ticker:
        return self.__ticker

    def put_quotecast(
        self,
        quotecast:Quotecast,
    ):
        matching_list = self.__matching_list
        fill_na = self.__fill_na
        metric_list_storage = self.__metric_list_storage

        metadata = quotecast.metadata
        json_data = quotecast.json_data

        # SETUP MATCHING LIST & METRIC LIST
        matching_list, metric_list = metric_handler.build_metric_list_from_json(
            json_data=json_data,
            matching_list=matching_list
        )

        # SETUP PRODUCT LIST
        product_list = metric_handler.extract_product_list(
            metric_list=matching_list
        )

        # SAVE MATCHING LIST
        self.__matching_list = matching_list

        # SETUP FILLED METRIC LIST
        if fill_na == True:
            metric_list_storage.put_metric_list(
                filled_metric_list=metric_list,
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