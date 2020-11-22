import datetime
import pandas as pd
import pickle
import random

from google.protobuf import json_format
from google.protobuf.message import Message
from quotecast.pb.quotecast_pb2 import Ticker
from typing import Dict, List

# pylint: disable=no-member

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)

def build_dict_from_ticker(
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
        ticker_dict[product].update(ticker.products[product].metrics)

    return ticker_dict

def build_df_from_ticker(
    ticker:Ticker,
    column_list:List[str]=[],
)->pd.DataFrame:
    ticker_dict = build_dict_from_ticker(
        ticker=ticker,
        column_list=column_list,
    )

    df = pd.DataFrame(ticker_dict.values())

    return df

def build_sample_ticker(
    number:int=10,
    metric_list:List[str]=['l1', 'l2' ,'l3'],
):
    """ Build a Ticker object for testing purpose. """

    # SETUP TICKER
    ticker = Ticker()
    ticker.metadata.response_datetime.GetCurrentTime()
    ticker.metadata.request_duration.FromNanoseconds(
        random.randrange(5*10**9)
    )

    # SETUP CTICKER - WITH EXTRA DATA

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

def build_dict_from_message(message:Message)->dict:
    message_dict = json_format.MessageToDict(
        message=message,
        including_default_value_fields=True,
        preserving_proto_field_name=True,
    )
    return message_dict

def save_object(
    obj:object,
    file_name:str,
    file_extension:str='.pickle',
):
    file_path = file_name + file_extension
    with open(file_path, 'wb') as f:
        pickle.dump(
            obj=obj,
            file=f,
            protocol=pickle.HIGHEST_PROTOCOL,
        )

def load_object(
    file_name:str,
    file_extension:str='.pickle',
)->object:
    file_path = file_name + file_extension
    with open(file_path, 'rb') as f:
        obj = pickle.load(file=f)

    return obj
