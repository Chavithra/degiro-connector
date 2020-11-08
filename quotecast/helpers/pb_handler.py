import pandas as pd

from google.protobuf import json_format
from quotecast.pb.quotecast_pb2 import (
    Ticker,
)
from typing import Dict, List
from google.protobuf.message import Message

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

if __name__ == '__main__':
    from IPython.display import display

    ticker = build_sample_ticker()

    df = build_df_from_ticker(ticker=ticker)
    display(df)
    record_list = build_dict_from_ticker(ticker=ticker)
    print(record_list)


























# TO KEEP : THESE FUNCTIONS MIGHT GET INTEGRATED INSIDE THE CONNECTOR

#     @classmethod
#     def get_filled_list(cls, ticker_list:list)->List[Ticker]:
#         if len(ticker_list) < 2:
#             raise AttributeError('There is nothing to fill.')

#         filled_list = list()
#         filled = Ticker()
#         filled.CopyFrom(ticker_list[0])

#         for index in range(1, len(ticker_list)):
#             filler = ticker_list[index]
#             filled = cls.fill_ticker(
#                 filled=filled,
#                 filler=filler,
#                 copy=True,
#             )
#             filled_list.append(filled)
        
#         return filled_list

#     @classmethod
#     def fill_ticker(
#             cls,
#             filled:Ticker,
#             filler:Ticker,
#             copy:bool=False,
#         )->Ticker:
#         if copy == True:
#             filled_copy = Ticker()
#             filled_copy.CopyFrom(filled)
#             filled = filled_copy

#         filled.metadata.MergeFrom(filler.metadata)
#         filled.product_list.MergeFrom(filler.product_list)

#         cls.fill_metric_list(
#             filled=filled,
#             filler=filler,
#         )

#         return filled

#     @classmethod
#     def fill_metric_list(
#             cls,
#             filled:Ticker,
#             filler:Ticker,
#         ):
#         metric_list = list()

#         for filler_metric in filler.metric_list:
#             filled_metric = cls.search_by_label(
#                 ticker=filled,
#                 label=filler_metric.label,
#             )

#             if filled_metric is None:
#                 metric = Metric()
#                 metric.CopyFrom(filler_metric)
#                 metric_list.append(metric)
#             else:
#                 filled_metric.value = filler_metric.value

#         filled.metric_list.extend(metric_list)



#     @classmethod
#     def build_df(
#             cls,
#             product_id:int,
#             ticker_list:List[Ticker],
#         )->pd.DataFrame:
#         """ Transform a list of ticker into a DataFrame. """

#         df_list = list()
#         for ticker in ticker_list:
#             df = TickerHelper.build_row(
#                 ticker=ticker,
#                 product_id=product_id,
#             )
#             df_list.append(df)

#         df = pd.concat(df_list, ignore_index=True)

#         return df

#     @classmethod
#     def build_row(
#             cls,
#             product_id:int,
#             ticker:Ticker,
#         )->pd.DataFrame:
#         """ Transform a Ticker object into a DataFrame. """

#         if ticker.ByteSize() <= 0:
#             df = pd.DataFrame(
#                 np.zeros(
#                     shape=(1, len(labels.MODEL)),
#                     dtype=np.float64
#                 ),
#                 columns=labels.MODEL,
#             )
#             return df
#         else:
#             rows = cls.build_dict(ticker=ticker)
#             row = rows[product_id]
#             row['request_duration'] = ticker.metadata.request_duration
#             row['response_time'] = cls.datetime_to_seconds(
#                 ticker.metadata.response_datetime
#             )
#             row['last_time'] = cls.time_to_seconds(row['LastTime'])
#             if 'LastPrice' in row:
#                 row['LastPrice_bis'] = row['LastPrice']
    
#             data = dict()
#             for label in labels.MODEL:
#                 if label in row:
#                     data[label] = row[label]
#                 else:
#                     data[label] = None

#             df = pd.DataFrame([data])
            
#             return df

#     @staticmethod
#     def datetime_to_time(date_time:str)->time.time:
#         t = date_time.split()[1]
#         return t

#     @staticmethod
#     def time_to_seconds(t:str)->float:
#         t = time.strptime(t,'%H:%M:%S')
#         seconds = datetime.timedelta(
#             hours=t.tm_hour,
#             minutes=t.tm_min,
#             seconds=t.tm_sec
#         ).total_seconds()

#         return seconds
    
#     @classmethod
#     def datetime_to_seconds(cls, date_time:str)->float:
#         t = cls.datetime_to_time(date_time)
#         seconds = cls.time_to_seconds(t)

#         return seconds

#     @staticmethod
#     def build_dict(
#             ticker:Ticker,
#         )->dict:
#         """ Transform a Ticker object into a dict
        
#         A Ticker as a "metric_list" containing Metric object.
#         Each Metric object as the attributes : "label" & "value".
#         The dict object key will be : the Metric "label".
#         The dict object value will be : the Metric "value".
#         Ticker following attributes are also copied :
#             * "product_list"
#             * "metadata"
#         """

#         groups = dict()
#         for metric in ticker.metric_list:
#             if not metric.product_id in groups:
#                 groups[metric.product_id] = dict()
#                 groups[metric.product_id]['product_id'] = metric.product_id
#             if metric.label in labels.METRIC:
#                 groups[metric.product_id][metric.label] = metric.value

#         groups['product_list'] = ticker.product_list
#         groups['metadata'] = ticker.metadata

#         return groups