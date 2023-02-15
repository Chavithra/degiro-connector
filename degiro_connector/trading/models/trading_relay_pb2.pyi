from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import wrappers_pb2 as _wrappers_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from degiro_connector.trading.models import trading_pb2 as _trading_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ConfirmOrder(_message.Message):
    __slots__ = ["confirmation_id", "order"]
    CONFIRMATION_ID_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    confirmation_id: _wrappers_pb2.StringValue
    order: _trading_pb2.Order
    def __init__(self, confirmation_id: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., order: _Optional[_Union[_trading_pb2.Order, _Mapping]] = ...) -> None: ...

class ProductSearch(_message.Message):
    __slots__ = ["bonds", "etfs", "funds", "futures", "leverageds", "lookup", "options", "stocks", "warrants"]
    BONDS_FIELD_NUMBER: _ClassVar[int]
    ETFS_FIELD_NUMBER: _ClassVar[int]
    FUNDS_FIELD_NUMBER: _ClassVar[int]
    FUTURES_FIELD_NUMBER: _ClassVar[int]
    LEVERAGEDS_FIELD_NUMBER: _ClassVar[int]
    LOOKUP_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    STOCKS_FIELD_NUMBER: _ClassVar[int]
    WARRANTS_FIELD_NUMBER: _ClassVar[int]
    bonds: _trading_pb2.ProductSearch.RequestBonds
    etfs: _trading_pb2.ProductSearch.RequestETFs
    funds: _trading_pb2.ProductSearch.RequestFunds
    futures: _trading_pb2.ProductSearch.RequestFutures
    leverageds: _trading_pb2.ProductSearch.RequestLeverageds
    lookup: _trading_pb2.ProductSearch.RequestLookup
    options: _trading_pb2.ProductSearch.RequestOptions
    stocks: _trading_pb2.ProductSearch.RequestStocks
    warrants: _trading_pb2.ProductSearch.RequestWarrants
    def __init__(self, bonds: _Optional[_Union[_trading_pb2.ProductSearch.RequestBonds, _Mapping]] = ..., etfs: _Optional[_Union[_trading_pb2.ProductSearch.RequestETFs, _Mapping]] = ..., funds: _Optional[_Union[_trading_pb2.ProductSearch.RequestFunds, _Mapping]] = ..., futures: _Optional[_Union[_trading_pb2.ProductSearch.RequestFutures, _Mapping]] = ..., leverageds: _Optional[_Union[_trading_pb2.ProductSearch.RequestLeverageds, _Mapping]] = ..., lookup: _Optional[_Union[_trading_pb2.ProductSearch.RequestLookup, _Mapping]] = ..., options: _Optional[_Union[_trading_pb2.ProductSearch.RequestOptions, _Mapping]] = ..., stocks: _Optional[_Union[_trading_pb2.ProductSearch.RequestStocks, _Mapping]] = ..., warrants: _Optional[_Union[_trading_pb2.ProductSearch.RequestWarrants, _Mapping]] = ...) -> None: ...

class SetConfig(_message.Message):
    __slots__ = ["auto_connect", "credentials"]
    AUTO_CONNECT_FIELD_NUMBER: _ClassVar[int]
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    auto_connect: bool
    credentials: _trading_pb2.Credentials
    def __init__(self, credentials: _Optional[_Union[_trading_pb2.Credentials, _Mapping]] = ..., auto_connect: bool = ...) -> None: ...
