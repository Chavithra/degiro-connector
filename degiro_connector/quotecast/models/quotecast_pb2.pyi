from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Chart(_message.Message):
    __slots__ = ["end", "requestid", "resolution", "series", "start"]
    class Interval(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class Request(_message.Message):
        __slots__ = ["culture", "override", "period", "requestid", "resolution", "series", "tz"]
        class OverrideEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: str
            def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
        CULTURE_FIELD_NUMBER: _ClassVar[int]
        OVERRIDE_FIELD_NUMBER: _ClassVar[int]
        PERIOD_FIELD_NUMBER: _ClassVar[int]
        REQUESTID_FIELD_NUMBER: _ClassVar[int]
        RESOLUTION_FIELD_NUMBER: _ClassVar[int]
        SERIES_FIELD_NUMBER: _ClassVar[int]
        TZ_FIELD_NUMBER: _ClassVar[int]
        culture: str
        override: _containers.ScalarMap[str, str]
        period: Chart.Interval
        requestid: str
        resolution: Chart.Interval
        series: _containers.RepeatedScalarFieldContainer[str]
        tz: str
        def __init__(self, requestid: _Optional[str] = ..., resolution: _Optional[_Union[Chart.Interval, str]] = ..., culture: _Optional[str] = ..., period: _Optional[_Union[Chart.Interval, str]] = ..., series: _Optional[_Iterable[str]] = ..., tz: _Optional[str] = ..., override: _Optional[_Mapping[str, str]] = ...) -> None: ...
    class Serie(_message.Message):
        __slots__ = ["data", "expires", "id", "times", "type"]
        DATA_FIELD_NUMBER: _ClassVar[int]
        EXPIRES_FIELD_NUMBER: _ClassVar[int]
        ID_FIELD_NUMBER: _ClassVar[int]
        TIMES_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        data: _struct_pb2.ListValue
        expires: str
        id: str
        times: str
        type: str
        def __init__(self, times: _Optional[str] = ..., expires: _Optional[str] = ..., data: _Optional[_Union[_struct_pb2.ListValue, _Mapping]] = ..., id: _Optional[str] = ..., type: _Optional[str] = ...) -> None: ...
    END_FIELD_NUMBER: _ClassVar[int]
    P10Y: Chart.Interval
    P1D: Chart.Interval
    P1M: Chart.Interval
    P1W: Chart.Interval
    P1Y: Chart.Interval
    P3M: Chart.Interval
    P3Y: Chart.Interval
    P50Y: Chart.Interval
    P5Y: Chart.Interval
    P6M: Chart.Interval
    PT15M: Chart.Interval
    PT15S: Chart.Interval
    PT1H: Chart.Interval
    PT1M: Chart.Interval
    PT1S: Chart.Interval
    PT30M: Chart.Interval
    PT30S: Chart.Interval
    PT5M: Chart.Interval
    PT60M: Chart.Interval
    REQUESTID_FIELD_NUMBER: _ClassVar[int]
    RESOLUTION_FIELD_NUMBER: _ClassVar[int]
    SERIES_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    YTD: Chart.Interval
    end: str
    requestid: str
    resolution: str
    series: _containers.RepeatedCompositeFieldContainer[Chart.Serie]
    start: str
    def __init__(self, requestid: _Optional[str] = ..., start: _Optional[str] = ..., end: _Optional[str] = ..., resolution: _Optional[str] = ..., series: _Optional[_Iterable[_Union[Chart.Serie, _Mapping]]] = ...) -> None: ...

class Metadata(_message.Message):
    __slots__ = ["request_duration", "response_datetime"]
    REQUEST_DURATION_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_DATETIME_FIELD_NUMBER: _ClassVar[int]
    request_duration: _duration_pb2.Duration
    response_datetime: _timestamp_pb2.Timestamp
    def __init__(self, response_datetime: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., request_duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...) -> None: ...

class Quotecast(_message.Message):
    __slots__ = ["json_data", "metadata"]
    class Request(_message.Message):
        __slots__ = ["subscriptions", "unsubscriptions"]
        class SubscriptionsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: _struct_pb2.ListValue
            def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.ListValue, _Mapping]] = ...) -> None: ...
        class UnsubscriptionsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: _struct_pb2.ListValue
            def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.ListValue, _Mapping]] = ...) -> None: ...
        SUBSCRIPTIONS_FIELD_NUMBER: _ClassVar[int]
        UNSUBSCRIPTIONS_FIELD_NUMBER: _ClassVar[int]
        subscriptions: _containers.MessageMap[str, _struct_pb2.ListValue]
        unsubscriptions: _containers.MessageMap[str, _struct_pb2.ListValue]
        def __init__(self, subscriptions: _Optional[_Mapping[str, _struct_pb2.ListValue]] = ..., unsubscriptions: _Optional[_Mapping[str, _struct_pb2.ListValue]] = ...) -> None: ...
    JSON_DATA_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    json_data: str
    metadata: Metadata
    def __init__(self, json_data: _Optional[str] = ..., metadata: _Optional[_Union[Metadata, _Mapping]] = ...) -> None: ...

class Ticker(_message.Message):
    __slots__ = ["metadata", "product_list", "products"]
    class Metrics(_message.Message):
        __slots__ = ["metrics"]
        class MetricsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: float
            def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
        METRICS_FIELD_NUMBER: _ClassVar[int]
        metrics: _containers.ScalarMap[str, float]
        def __init__(self, metrics: _Optional[_Mapping[str, float]] = ...) -> None: ...
    class ProductsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Ticker.Metrics
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Ticker.Metrics, _Mapping]] = ...) -> None: ...
    METADATA_FIELD_NUMBER: _ClassVar[int]
    PRODUCTS_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_LIST_FIELD_NUMBER: _ClassVar[int]
    metadata: Metadata
    product_list: _containers.RepeatedScalarFieldContainer[str]
    products: _containers.MessageMap[str, Ticker.Metrics]
    def __init__(self, metadata: _Optional[_Union[Metadata, _Mapping]] = ..., products: _Optional[_Mapping[str, Ticker.Metrics]] = ..., product_list: _Optional[_Iterable[str]] = ...) -> None: ...
