import pandas as pd
import pickle

from google.protobuf import json_format
from google.protobuf.message import Message
from quotecast.pb.quotecast_pb2 import Quotecast, NewTicker, Ticker
from typing import Dict, List

# pylint: disable=no-member

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)

def add_unset_column_list(
    record:Dict[str, str],
    column_list:List[str],
)->Dict[str, str]:
    """ Make sure the dict contains all the keys.

    Args:
        record (dict):
            Record which might not have all the fields set.
    Returns:
        dict:
            Record with undefined fields set as None.
    """

    if len(record) <= 3:
        raise AttributeError(
            'Can\'t convert this record into any useful.'
        )

    empty_list = [None] * len(column_list)
    complete_record = dict(zip(column_list, empty_list))
    complete_record.update(record)

    return complete_record

def build_dict_from_ticker(
    ticker:Ticker,
    df_column_list:List[str]=[],
)->List[Dict[str, str]]:
    metadata = ticker.metadata
    metric_list = ticker.metric_list

    # GROUP BY PRODUCT
    product_list = dict()
    for metric in metric_list:
        if metric.product_id == 0:
            continue
        elif not metric.product_id in product_list:
            product_list[metric.product_id] = dict()
            product_list[metric.product_id]['product_id'] = metric.product_id
            product_list[metric.product_id]['response_datetime'] = metadata.response_datetime
            product_list[metric.product_id]['request_duration'] = metadata.request_duration
            product_list[metric.product_id][metric.label] = metric.value
        else:
            product_list[metric.product_id][metric.label] = metric.value

    # BUILD RECORDS LIST
    record_list = list()
    for record in product_list.values():
        if len(df_column_list) > 0:
            # APPEND EMPTY COLUMNS
            complete_record = add_unset_column_list(
                record=record,
                column_list=df_column_list,
            )
            record_list.append(complete_record)
        else:
            record_list.append(record)

    return record_list


def build_df_from_ticker(
    ticker:Ticker,
    df_column_list:List[str]=[],
)->pd.DataFrame:
    record_list = build_dict_from_ticker(
        ticker=ticker,
        df_column_list=df_column_list,
    )

    df = pd.DataFrame(record_list)

    return df

def build_sample_ticker():
    """ Build a Ticker object for testing purpose. """

    # SETUP TICKER
    # ticker_serialized = b'\n\x13\x10\xf7\\\x1a\x077028750 \xf7\\*\x02id\n\x19\x10\xf7\\\x1a\x0511895 \xf7\\*\nproduct_id\n\x18\x10\xf7\\\x1a\x062580.0 \xf7\\*\x08A7Volume\n\x18\x10\xf7\\\x1a\x061396.0 \xf7\\*\x08A9Volume\n\x18\x10\xf7\\\x1a\x063130.0 \xf7\\*\x08B7Volume\x12\x02\xf7\\\x1a\x1e\n\x132020-07-02 09:14:59\x11\xe3\xfcM(D@\xf0?'
    ticker_serialized = b'\n\x13\x10\xf7\\\x1a\x077015720 \xf7\\*\x02id\n\x19\x10\xf7\\\x1a\x0511895 \xf7\\*\nproduct_id\n\x1c\x10\xf7\\\x1a\n2020-07-02 \xf7\\*\x08LastDate\n\x19\x10\xf7\\\x1a\x079:00:17 \xf7\\*\x08LastTime\n\x17\x10\xf7\\\x1a\x049.45 \xf7\\*\tLastPrice\n\x18\x10\xf7\\\x1a\x0470.0 \xf7\\*\nLastVolume\n\x16\x10\xf7\\\x1a\x059.484 \xf7\\*\x07A1Price\n\x16\x10\xf7\\\x1a\x059.498 \xf7\\*\x07A2Price\n\x14\x10\xf7\\\x1a\x039.5 \xf7\\*\x07A3Price\n\x16\x10\xf7\\\x1a\x059.514 \xf7\\*\x07A4Price\n\x16\x10\xf7\\\x1a\x059.515 \xf7\\*\x07A5Price\n\x15\x10\xf7\\\x1a\x049.52 \xf7\\*\x07A6Price\n\x16\x10\xf7\\\x1a\x059.532 \xf7\\*\x07A7Price\n\x15\x10\xf7\\\x1a\x049.54 \xf7\\*\x07A8Price\n\x16\x10\xf7\\\x1a\x059.549 \xf7\\*\x07A9Price\n\x16\x10\xf7\\\x1a\x049.55 \xf7\\*\x08A10Price\n\x18\x10\xf7\\\x1a\x062123.0 \xf7\\*\x08A1Volume\n\x18\x10\xf7\\\x1a\x063000.0 \xf7\\*\x08A2Volume\n\x17\x10\xf7\\\x1a\x05155.0 \xf7\\*\x08A3Volume\n\x17\x10\xf7\\\x1a\x05682.0 \xf7\\*\x08A4Volume\n\x17\x10\xf7\\\x1a\x05600.0 \xf7\\*\x08A5Volume\n\x18\x10\xf7\\\x1a\x067994.0 \xf7\\*\x08A6Volume\n\x18\x10\xf7\\\x1a\x063000.0 \xf7\\*\x08A7Volume\n\x18\x10\xf7\\\x1a\x061097.0 \xf7\\*\x08A8Volume\n\x18\x10\xf7\\\x1a\x065282.0 \xf7\\*\x08A9Volume\n\x18\x10\xf7\\\x1a\x05150.0 \xf7\\*\tA10Volume\n\x15\x10\xf7\\\x1a\x049.45 \xf7\\*\x07B1Price\n\x16\x10\xf7\\\x1a\x059.446 \xf7\\*\x07B2Price\n\x16\x10\xf7\\\x1a\x059.444 \xf7\\*\x07B3Price\n\x16\x10\xf7\\\x1a\x059.439 \xf7\\*\x07B4Price\n\x15\x10\xf7\\\x1a\x049.43 \xf7\\*\x07B5Price\n\x15\x10\xf7\\\x1a\x049.42 \xf7\\*\x07B6Price\n\x15\x10\xf7\\\x1a\x049.41 \xf7\\*\x07B7Price\n\x14\x10\xf7\\\x1a\x039.4 \xf7\\*\x07B8Price\n\x16\x10\xf7\\\x1a\x059.396 \xf7\\*\x07B9Price\n\x17\x10\xf7\\\x1a\x059.394 \xf7\\*\x08B10Price\n\x17\x10\xf7\\\x1a\x05323.0 \xf7\\*\x08B1Volume\n\x18\x10\xf7\\\x1a\x062704.0 \xf7\\*\x08B2Volume\n\x17\x10\xf7\\\x1a\x05388.0 \xf7\\*\x08B3Volume\n\x16\x10\xf7\\\x1a\x0497.0 \xf7\\*\x08B4Volume\n\x17\x10\xf7\\\x1a\x05400.0 \xf7\\*\x08B5Volume\n\x18\x10\xf7\\\x1a\x062802.0 \xf7\\*\x08B6Volume\n\x18\x10\xf7\\\x1a\x063500.0 \xf7\\*\x08B7Volume\n\x18\x10\xf7\\\x1a\x067646.0 \xf7\\*\x08B8Volume\n\x17\x10\xf7\\\x1a\x05347.0 \xf7\\*\x08B9Volume\n\x18\x10\xf7\\\x1a\x05347.0 \xf7\\*\tB10Volume\x12\x02\xf7\\\x1a\x1e\n\x132020-07-02 09:00:17\x11\xfd\xbc\xa9H\x851\xf0?'
    ticker = Ticker()
    ticker.ParseFromString(ticker_serialized)

    # SETUP CTICKER - WITH EXTRA DATA
    cticker = Ticker()
    cticker.CopyFrom(ticker)
    for metric in cticker.metric_list:
        metric.reference = 123
        metric.product_id = 123
        if metric.label == 'product_id':
            metric.value = "123"

    cticker.metric_list.extend(ticker.metric_list)

    return cticker

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
