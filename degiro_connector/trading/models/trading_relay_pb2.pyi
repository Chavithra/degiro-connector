"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import degiro_connector.trading.models.trading_pb2
import google.protobuf.descriptor
import google.protobuf.message
import google.protobuf.wrappers_pb2
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor = ...

class SetConfig(google.protobuf.message.Message):
    """MESSAGES"""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    CREDENTIALS_FIELD_NUMBER: builtins.int
    AUTO_CONNECT_FIELD_NUMBER: builtins.int
    @property
    def credentials(self) -> degiro_connector.trading.models.trading_pb2.Credentials: ...
    auto_connect: builtins.bool = ...
    def __init__(self,
        *,
        credentials : typing.Optional[degiro_connector.trading.models.trading_pb2.Credentials] = ...,
        auto_connect : builtins.bool = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal[u"credentials",b"credentials"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal[u"auto_connect",b"auto_connect",u"credentials",b"credentials"]) -> None: ...
global___SetConfig = SetConfig

class ConfirmOrder(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    CONFIRMATION_ID_FIELD_NUMBER: builtins.int
    ORDER_FIELD_NUMBER: builtins.int
    @property
    def confirmation_id(self) -> google.protobuf.wrappers_pb2.StringValue: ...
    @property
    def order(self) -> degiro_connector.trading.models.trading_pb2.Order: ...
    def __init__(self,
        *,
        confirmation_id : typing.Optional[google.protobuf.wrappers_pb2.StringValue] = ...,
        order : typing.Optional[degiro_connector.trading.models.trading_pb2.Order] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal[u"confirmation_id",b"confirmation_id",u"order",b"order"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal[u"confirmation_id",b"confirmation_id",u"order",b"order"]) -> None: ...
global___ConfirmOrder = ConfirmOrder

class ProductSearch(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    BONDS_FIELD_NUMBER: builtins.int
    ETFS_FIELD_NUMBER: builtins.int
    FUNDS_FIELD_NUMBER: builtins.int
    FUTURES_FIELD_NUMBER: builtins.int
    LEVERAGEDS_FIELD_NUMBER: builtins.int
    LOOKUP_FIELD_NUMBER: builtins.int
    OPTIONS_FIELD_NUMBER: builtins.int
    STOCKS_FIELD_NUMBER: builtins.int
    WARRANTS_FIELD_NUMBER: builtins.int
    @property
    def bonds(self) -> degiro_connector.trading.models.trading_pb2.ProductSearch.RequestBonds: ...
    @property
    def etfs(self) -> degiro_connector.trading.models.trading_pb2.ProductSearch.RequestETFs: ...
    @property
    def funds(self) -> degiro_connector.trading.models.trading_pb2.ProductSearch.RequestFunds: ...
    @property
    def futures(self) -> degiro_connector.trading.models.trading_pb2.ProductSearch.RequestFutures: ...
    @property
    def leverageds(self) -> degiro_connector.trading.models.trading_pb2.ProductSearch.RequestLeverageds: ...
    @property
    def lookup(self) -> degiro_connector.trading.models.trading_pb2.ProductSearch.RequestLookup: ...
    @property
    def options(self) -> degiro_connector.trading.models.trading_pb2.ProductSearch.RequestOptions: ...
    @property
    def stocks(self) -> degiro_connector.trading.models.trading_pb2.ProductSearch.RequestStocks: ...
    @property
    def warrants(self) -> degiro_connector.trading.models.trading_pb2.ProductSearch.RequestWarrants: ...
    def __init__(self,
        *,
        bonds : typing.Optional[degiro_connector.trading.models.trading_pb2.ProductSearch.RequestBonds] = ...,
        etfs : typing.Optional[degiro_connector.trading.models.trading_pb2.ProductSearch.RequestETFs] = ...,
        funds : typing.Optional[degiro_connector.trading.models.trading_pb2.ProductSearch.RequestFunds] = ...,
        futures : typing.Optional[degiro_connector.trading.models.trading_pb2.ProductSearch.RequestFutures] = ...,
        leverageds : typing.Optional[degiro_connector.trading.models.trading_pb2.ProductSearch.RequestLeverageds] = ...,
        lookup : typing.Optional[degiro_connector.trading.models.trading_pb2.ProductSearch.RequestLookup] = ...,
        options : typing.Optional[degiro_connector.trading.models.trading_pb2.ProductSearch.RequestOptions] = ...,
        stocks : typing.Optional[degiro_connector.trading.models.trading_pb2.ProductSearch.RequestStocks] = ...,
        warrants : typing.Optional[degiro_connector.trading.models.trading_pb2.ProductSearch.RequestWarrants] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal[u"bonds",b"bonds",u"etfs",b"etfs",u"funds",b"funds",u"futures",b"futures",u"leverageds",b"leverageds",u"lookup",b"lookup",u"options",b"options",u"request",b"request",u"stocks",b"stocks",u"warrants",b"warrants"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal[u"bonds",b"bonds",u"etfs",b"etfs",u"funds",b"funds",u"futures",b"futures",u"leverageds",b"leverageds",u"lookup",b"lookup",u"options",b"options",u"request",b"request",u"stocks",b"stocks",u"warrants",b"warrants"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal[u"request",b"request"]) -> typing.Optional[typing_extensions.Literal["bonds","etfs","funds","futures","leverageds","lookup","options","stocks","warrants"]]: ...
global___ProductSearch = ProductSearch