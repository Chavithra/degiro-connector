import logging

from quotecast.pb.quotecast_pb2 import (
    Metric,
)
from typing import List
from wrapt.decorators import synchronized

class MetricListSorage:
    """  Degiro's API send only the metrics which change.
    Metrics are stored here so the full metric list can be retrieved.
    """

    def __init__(
        self,
    ):
        self.__logger = logging.getLogger(self.__module__)
        self.__metric_dict = dict()

    @property
    def metric_dict(self)->List[Metric]:
        return self.__metric_dict

    def get_metric_list(
        self,
        product_list:List[int],
    )->List[Metric]:
        metric_dict = self.__metric_dict

        metric_list = list()

        for product_id in product_list:
            if product_id in metric_dict:
                metric_list.extend(metric_dict[product_id].values())

        return metric_list

    def put_metric_list(
        self,
        metric_list:List[Metric],
    ):
        metric_dict = self.__metric_dict

        for metric in metric_list:
            product_id = metric.product_id
            label = metric.label

            if product_id == 0:
                continue
            elif not product_id in metric_dict:
                metric_dict[product_id] = dict()
                metric_dict[product_id][label] = metric
            else:
                metric_dict[product_id][label] = metric