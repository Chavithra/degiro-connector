import pandas as pd
import random

from google.protobuf import json_format
from google.protobuf.message import Message
from quotecast.pb.quotecast_pb2 import Request, Ticker
from typing import Dict, List

# pylint: disable=no-member

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)

def ticker_to_dict(
    ticker:Ticker,
    column_list:List[str]=[],
)->List[Dict[str, str]]:
    empty_list = [None] * len(column_list)
    empty_metrics = dict(zip(column_list, empty_list))
    empty_metrics['response_datetime'] = \
        ticker.metadata.response_datetime.ToJsonString()
    empty_metrics['request_duration'] = \
        ticker.metadata.request_duration.ToMicroseconds()/10**6

    ticker_dict = dict()
    for product in ticker.products:
        ticker_dict[product] = empty_metrics.copy()
        ticker_dict[product]['vwd_id'] = product
        ticker_dict[product].update(ticker.products[product].metrics)

    return ticker_dict

def ticker_to_df(
    ticker:Ticker,
    column_list:List[str]=[],
)->pd.DataFrame:
    ticker_dict = ticker_to_dict(
        ticker=ticker,
        column_list=column_list,
    )

    df = pd.DataFrame(ticker_dict.values())

    return df

def build_ticker_sample(
    number:int=10,
    metric_list:List[str]=['l1', 'l2' ,'l3'],
):
    """ Build a Ticker object for testing purpose. """

    ticker = Ticker()

    # SETUP METADATA
    ticker.metadata.response_datetime.GetCurrentTime()
    ticker.metadata.request_duration.FromNanoseconds(
        random.randrange(5*10**9)
    )

    # SETUP EXTRA-DATA
    for i in range(number):
        for metric in metric_list:
            ticker.products[i].metrics[metric] = random.uniform(
                0.,
                100.
            )

    return ticker

def merge_tickers(
    ticker1:Ticker,
    ticker2:Ticker,
    update_only:bool=False,
):
    """ Override metrics of ticker1 with ticker2's metrics.

    Args:
        ticker1 (Ticker): Ticker to fill.
        ticker2 (Ticker): Ticker used to fill.
        update_only (bool, optional):
            Whether or not we want to add products from "ticker2" to
            "ticker1".
    """

    if update_only == True:
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

def message_to_dict(message:Message)->dict:
    return json_format.MessageToDict(
        message=message,
        including_default_value_fields=True,
        preserving_proto_field_name=True,
        use_integers_for_enums=True,
        descriptor_pool=None,
        float_precision=None,
    )

def update_message_from_dict(message:Message, js_dict:dict)->Message:
    json_format.ParseDict(
        js_dict=js_dict,
        message=message,
        ignore_unknown_fields=True,
        descriptor_pool=None,
    )

def request_to_api(request:Request)->str:
    payload = '{"controlData":"'
    for vwd_id in request.subscriptions:
        for metric_name in request.subscriptions[vwd_id].metrics:
            payload += 'a_req(' + vwd_id + '.' + metric_name + ');'
    for vwd_id in request.unsubscriptions:
        for metric_name in request.unsubscriptions[vwd_id].metrics:
            payload += 'a_rel(' + vwd_id + '.' + metric_name + ');'
    payload += '"}'

    return payload