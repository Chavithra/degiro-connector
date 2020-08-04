import json
import logging


from quotecast.helpers.metrics_parser import (
    MetricsParser
)
from quotecast.pb.quotecast_pb2 import (
    Matching,
    Metadata,
    Metric,
    RawResponse,
    Ticker,
)
from typing import List

class RawResponseParser:
    @classmethod
    def parse(
            cls,
            raw_response:RawResponse,
            matching_list:List[Matching]
        )->(list, Ticker):

        metadata = raw_response.metadata
        matching_list, metric_list = MetricsParser.parse(
            data=raw_response.response_json,
            matching_list=matching_list
        )
        product_list = MetricsParser.extract_product_list(
            metric_list=matching_list
        )
        ticker = Ticker(
            metric_list=metric_list,
            product_list=product_list,
            metadata=metadata
        )

        return matching_list, ticker