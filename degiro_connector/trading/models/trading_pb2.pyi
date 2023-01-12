from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AccountOverview(_message.Message):
    __slots__ = ["response_datetime", "values"]
    class Request(_message.Message):
        __slots__ = ["from_date", "to_date"]
        class Date(_message.Message):
            __slots__ = ["day", "month", "year"]
            DAY_FIELD_NUMBER: _ClassVar[int]
            MONTH_FIELD_NUMBER: _ClassVar[int]
            YEAR_FIELD_NUMBER: _ClassVar[int]
            day: int
            month: int
            year: int
            def __init__(self, year: _Optional[int] = ..., month: _Optional[int] = ..., day: _Optional[int] = ...) -> None: ...
        FROM_DATE_FIELD_NUMBER: _ClassVar[int]
        TO_DATE_FIELD_NUMBER: _ClassVar[int]
        from_date: AccountOverview.Request.Date
        to_date: AccountOverview.Request.Date
        def __init__(self, from_date: _Optional[_Union[AccountOverview.Request.Date, _Mapping]] = ..., to_date: _Optional[_Union[AccountOverview.Request.Date, _Mapping]] = ...) -> None: ...
    RESPONSE_DATETIME_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    response_datetime: _timestamp_pb2.Timestamp
    values: _struct_pb2.Struct
    def __init__(self, values: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., response_datetime: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class Agenda(_message.Message):
    __slots__ = ["calendar_type", "items", "offset", "response_datetime", "total"]
    class CalendarType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class Request(_message.Message):
        __slots__ = ["calendar_type", "classifications", "company_name", "countries", "end_date", "limit", "offset", "order_by_desc", "start_date", "units"]
        CALENDAR_TYPE_FIELD_NUMBER: _ClassVar[int]
        CLASSIFICATIONS_FIELD_NUMBER: _ClassVar[int]
        COMPANY_NAME_FIELD_NUMBER: _ClassVar[int]
        COUNTRIES_FIELD_NUMBER: _ClassVar[int]
        END_DATE_FIELD_NUMBER: _ClassVar[int]
        LIMIT_FIELD_NUMBER: _ClassVar[int]
        OFFSET_FIELD_NUMBER: _ClassVar[int]
        ORDER_BY_DESC_FIELD_NUMBER: _ClassVar[int]
        START_DATE_FIELD_NUMBER: _ClassVar[int]
        UNITS_FIELD_NUMBER: _ClassVar[int]
        calendar_type: Agenda.CalendarType
        classifications: str
        company_name: str
        countries: str
        end_date: _timestamp_pb2.Timestamp
        limit: int
        offset: int
        order_by_desc: bool
        start_date: _timestamp_pb2.Timestamp
        units: str
        def __init__(self, calendar_type: _Optional[_Union[Agenda.CalendarType, str]] = ..., offset: _Optional[int] = ..., limit: _Optional[int] = ..., order_by_desc: bool = ..., start_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., company_name: _Optional[str] = ..., countries: _Optional[str] = ..., classifications: _Optional[str] = ..., units: _Optional[str] = ...) -> None: ...
    CALENDAR_TYPE_FIELD_NUMBER: _ClassVar[int]
    DIVIDEND_CALENDAR: Agenda.CalendarType
    EARNINGS_CALENDAR: Agenda.CalendarType
    ECONOMIC_CALENDAR: Agenda.CalendarType
    HOLIDAY_CALENDAR: Agenda.CalendarType
    IPO_CALENDAR: Agenda.CalendarType
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_DATETIME_FIELD_NUMBER: _ClassVar[int]
    SPLIT_CALENDAR: Agenda.CalendarType
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    calendar_type: Agenda.CalendarType
    items: _containers.RepeatedCompositeFieldContainer[_struct_pb2.Struct]
    offset: int
    response_datetime: _timestamp_pb2.Timestamp
    total: int
    def __init__(self, calendar_type: _Optional[_Union[Agenda.CalendarType, str]] = ..., items: _Optional[_Iterable[_Union[_struct_pb2.Struct, _Mapping]]] = ..., offset: _Optional[int] = ..., total: _Optional[int] = ..., response_datetime: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class CashAccountReport(_message.Message):
    __slots__ = ["content", "format", "response_datetime"]
    class Format(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class Request(_message.Message):
        __slots__ = ["country", "format", "from_date", "lang", "to_date"]
        class Date(_message.Message):
            __slots__ = ["day", "month", "year"]
            DAY_FIELD_NUMBER: _ClassVar[int]
            MONTH_FIELD_NUMBER: _ClassVar[int]
            YEAR_FIELD_NUMBER: _ClassVar[int]
            day: int
            month: int
            year: int
            def __init__(self, year: _Optional[int] = ..., month: _Optional[int] = ..., day: _Optional[int] = ...) -> None: ...
        COUNTRY_FIELD_NUMBER: _ClassVar[int]
        FORMAT_FIELD_NUMBER: _ClassVar[int]
        FROM_DATE_FIELD_NUMBER: _ClassVar[int]
        LANG_FIELD_NUMBER: _ClassVar[int]
        TO_DATE_FIELD_NUMBER: _ClassVar[int]
        country: str
        format: CashAccountReport.Format
        from_date: CashAccountReport.Request.Date
        lang: str
        to_date: CashAccountReport.Request.Date
        def __init__(self, format: _Optional[_Union[CashAccountReport.Format, str]] = ..., country: _Optional[str] = ..., lang: _Optional[str] = ..., from_date: _Optional[_Union[CashAccountReport.Request.Date, _Mapping]] = ..., to_date: _Optional[_Union[CashAccountReport.Request.Date, _Mapping]] = ...) -> None: ...
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    CSV: CashAccountReport.Format
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    HTML: CashAccountReport.Format
    PDF: CashAccountReport.Format
    RESPONSE_DATETIME_FIELD_NUMBER: _ClassVar[int]
    XLS: CashAccountReport.Format
    content: str
    format: CashAccountReport.Format
    response_datetime: _timestamp_pb2.Timestamp
    def __init__(self, content: _Optional[str] = ..., format: _Optional[_Union[CashAccountReport.Format, str]] = ..., response_datetime: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class CompanyProfile(_message.Message):
    __slots__ = ["values"]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _struct_pb2.Struct
    def __init__(self, values: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class CompanyRatios(_message.Message):
    __slots__ = ["values"]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _struct_pb2.Struct
    def __init__(self, values: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class Credentials(_message.Message):
    __slots__ = ["int_account", "one_time_password", "password", "totp_secret_key", "username"]
    INT_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    ONE_TIME_PASSWORD_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    TOTP_SECRET_KEY_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    int_account: int
    one_time_password: int
    password: str
    totp_secret_key: str
    username: str
    def __init__(self, int_account: _Optional[int] = ..., username: _Optional[str] = ..., password: _Optional[str] = ..., totp_secret_key: _Optional[str] = ..., one_time_password: _Optional[int] = ...) -> None: ...

class EstimatesSummaries(_message.Message):
    __slots__ = ["annual", "currency", "interim", "lastRetrieved", "lastUpdated", "preferredMeasure", "ric"]
    ANNUAL_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    INTERIM_FIELD_NUMBER: _ClassVar[int]
    LASTRETRIEVED_FIELD_NUMBER: _ClassVar[int]
    LASTUPDATED_FIELD_NUMBER: _ClassVar[int]
    PREFERREDMEASURE_FIELD_NUMBER: _ClassVar[int]
    RIC_FIELD_NUMBER: _ClassVar[int]
    annual: _containers.RepeatedCompositeFieldContainer[_struct_pb2.Struct]
    currency: str
    interim: _containers.RepeatedCompositeFieldContainer[_struct_pb2.Struct]
    lastRetrieved: str
    lastUpdated: str
    preferredMeasure: str
    ric: str
    def __init__(self, annual: _Optional[_Iterable[_Union[_struct_pb2.Struct, _Mapping]]] = ..., currency: _Optional[str] = ..., interim: _Optional[_Iterable[_Union[_struct_pb2.Struct, _Mapping]]] = ..., lastRetrieved: _Optional[str] = ..., lastUpdated: _Optional[str] = ..., preferredMeasure: _Optional[str] = ..., ric: _Optional[str] = ...) -> None: ...

class Favourites(_message.Message):
    __slots__ = ["response_datetime", "values"]
    class List(_message.Message):
        __slots__ = ["id", "is_default", "name", "product_ids"]
        ID_FIELD_NUMBER: _ClassVar[int]
        IS_DEFAULT_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        PRODUCT_IDS_FIELD_NUMBER: _ClassVar[int]
        id: int
        is_default: bool
        name: str
        product_ids: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., is_default: bool = ..., product_ids: _Optional[_Iterable[int]] = ...) -> None: ...
    RESPONSE_DATETIME_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    response_datetime: _timestamp_pb2.Timestamp
    values: _containers.RepeatedCompositeFieldContainer[Favourites.List]
    def __init__(self, values: _Optional[_Iterable[_Union[Favourites.List, _Mapping]]] = ..., response_datetime: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class FinancialStatements(_message.Message):
    __slots__ = ["values"]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _struct_pb2.Struct
    def __init__(self, values: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class LatestNews(_message.Message):
    __slots__ = ["items", "offset", "total"]
    class Request(_message.Message):
        __slots__ = ["languages", "limit", "offset"]
        LANGUAGES_FIELD_NUMBER: _ClassVar[int]
        LIMIT_FIELD_NUMBER: _ClassVar[int]
        OFFSET_FIELD_NUMBER: _ClassVar[int]
        languages: str
        limit: int
        offset: int
        def __init__(self, offset: _Optional[int] = ..., languages: _Optional[str] = ..., limit: _Optional[int] = ...) -> None: ...
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[_struct_pb2.Struct]
    offset: int
    total: int
    def __init__(self, items: _Optional[_Iterable[_Union[_struct_pb2.Struct, _Mapping]]] = ..., offset: _Optional[int] = ..., total: _Optional[int] = ...) -> None: ...

class NewsByCompany(_message.Message):
    __slots__ = ["items", "offset", "total"]
    class Request(_message.Message):
        __slots__ = ["isin", "languages", "limit", "offset"]
        ISIN_FIELD_NUMBER: _ClassVar[int]
        LANGUAGES_FIELD_NUMBER: _ClassVar[int]
        LIMIT_FIELD_NUMBER: _ClassVar[int]
        OFFSET_FIELD_NUMBER: _ClassVar[int]
        isin: str
        languages: str
        limit: int
        offset: int
        def __init__(self, isin: _Optional[str] = ..., limit: _Optional[int] = ..., offset: _Optional[int] = ..., languages: _Optional[str] = ...) -> None: ...
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[_struct_pb2.Struct]
    offset: int
    total: int
    def __init__(self, items: _Optional[_Iterable[_Union[_struct_pb2.Struct, _Mapping]]] = ..., offset: _Optional[int] = ..., total: _Optional[int] = ...) -> None: ...

class Order(_message.Message):
    __slots__ = ["action", "contract_size", "contract_type", "currency", "hour", "id", "is_deletable", "is_modifiable", "order_type", "price", "product", "product_id", "quantity", "retained_order", "sent_to_exchange", "size", "stop_price", "time_type", "total_order_value"]
    class Action(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class OrderType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class TimeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class CheckingResponse(_message.Message):
        __slots__ = ["auto_fx_conversion_rate", "confirmation_id", "free_space_new", "response_datetime", "show_ex_ante_report_link", "transaction_auto_fx_opposite_surcharges", "transaction_auto_fx_surcharges", "transaction_fee", "transaction_fees", "transaction_opposite_fees", "transaction_taxes"]
        AUTO_FX_CONVERSION_RATE_FIELD_NUMBER: _ClassVar[int]
        CONFIRMATION_ID_FIELD_NUMBER: _ClassVar[int]
        FREE_SPACE_NEW_FIELD_NUMBER: _ClassVar[int]
        RESPONSE_DATETIME_FIELD_NUMBER: _ClassVar[int]
        SHOW_EX_ANTE_REPORT_LINK_FIELD_NUMBER: _ClassVar[int]
        TRANSACTION_AUTO_FX_OPPOSITE_SURCHARGES_FIELD_NUMBER: _ClassVar[int]
        TRANSACTION_AUTO_FX_SURCHARGES_FIELD_NUMBER: _ClassVar[int]
        TRANSACTION_FEES_FIELD_NUMBER: _ClassVar[int]
        TRANSACTION_FEE_FIELD_NUMBER: _ClassVar[int]
        TRANSACTION_OPPOSITE_FEES_FIELD_NUMBER: _ClassVar[int]
        TRANSACTION_TAXES_FIELD_NUMBER: _ClassVar[int]
        auto_fx_conversion_rate: float
        confirmation_id: str
        free_space_new: float
        response_datetime: _timestamp_pb2.Timestamp
        show_ex_ante_report_link: bool
        transaction_auto_fx_opposite_surcharges: _containers.RepeatedCompositeFieldContainer[_struct_pb2.Struct]
        transaction_auto_fx_surcharges: _containers.RepeatedCompositeFieldContainer[_struct_pb2.Struct]
        transaction_fee: float
        transaction_fees: _containers.RepeatedCompositeFieldContainer[_struct_pb2.Struct]
        transaction_opposite_fees: _containers.RepeatedCompositeFieldContainer[_struct_pb2.Struct]
        transaction_taxes: _containers.RepeatedCompositeFieldContainer[_struct_pb2.Struct]
        def __init__(self, confirmation_id: _Optional[str] = ..., free_space_new: _Optional[float] = ..., response_datetime: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., transaction_fees: _Optional[_Iterable[_Union[_struct_pb2.Struct, _Mapping]]] = ..., transaction_opposite_fees: _Optional[_Iterable[_Union[_struct_pb2.Struct, _Mapping]]] = ..., transaction_taxes: _Optional[_Iterable[_Union[_struct_pb2.Struct, _Mapping]]] = ..., transaction_auto_fx_surcharges: _Optional[_Iterable[_Union[_struct_pb2.Struct, _Mapping]]] = ..., transaction_auto_fx_opposite_surcharges: _Optional[_Iterable[_Union[_struct_pb2.Struct, _Mapping]]] = ..., auto_fx_conversion_rate: _Optional[float] = ..., transaction_fee: _Optional[float] = ..., show_ex_ante_report_link: bool = ...) -> None: ...
    class ConfirmationResponse(_message.Message):
        __slots__ = ["order_id", "response_datetime"]
        ORDER_ID_FIELD_NUMBER: _ClassVar[int]
        RESPONSE_DATETIME_FIELD_NUMBER: _ClassVar[int]
        order_id: str
        response_datetime: _timestamp_pb2.Timestamp
        def __init__(self, order_id: _Optional[str] = ..., response_datetime: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
    ACTION_FIELD_NUMBER: _ClassVar[int]
    BUY: Order.Action
    CONTRACT_SIZE_FIELD_NUMBER: _ClassVar[int]
    CONTRACT_TYPE_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    GOOD_TILL_CANCELED: Order.TimeType
    GOOD_TILL_DAY: Order.TimeType
    HOUR_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    IS_DELETABLE_FIELD_NUMBER: _ClassVar[int]
    IS_MODIFIABLE_FIELD_NUMBER: _ClassVar[int]
    LIMIT: Order.OrderType
    MARKET: Order.OrderType
    ORDER_TYPE_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_ID_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    RETAINED_ORDER_FIELD_NUMBER: _ClassVar[int]
    SELL: Order.Action
    SENT_TO_EXCHANGE_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    STOP_LIMIT: Order.OrderType
    STOP_LOSS: Order.OrderType
    STOP_PRICE_FIELD_NUMBER: _ClassVar[int]
    TIME_TYPE_FIELD_NUMBER: _ClassVar[int]
    TOTAL_ORDER_VALUE_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN_0: Order.TimeType
    UNKNOWN_2: Order.TimeType
    action: Order.Action
    contract_size: float
    contract_type: int
    currency: str
    hour: str
    id: str
    is_deletable: bool
    is_modifiable: bool
    order_type: Order.OrderType
    price: float
    product: str
    product_id: int
    quantity: float
    retained_order: bool
    sent_to_exchange: bool
    size: float
    stop_price: float
    time_type: Order.TimeType
    total_order_value: float
    def __init__(self, action: _Optional[_Union[Order.Action, str]] = ..., id: _Optional[str] = ..., order_type: _Optional[_Union[Order.OrderType, str]] = ..., price: _Optional[float] = ..., stop_price: _Optional[float] = ..., product_id: _Optional[int] = ..., size: _Optional[float] = ..., time_type: _Optional[_Union[Order.TimeType, str]] = ..., contract_size: _Optional[float] = ..., contract_type: _Optional[int] = ..., currency: _Optional[str] = ..., hour: _Optional[str] = ..., is_deletable: bool = ..., is_modifiable: bool = ..., product: _Optional[str] = ..., quantity: _Optional[float] = ..., total_order_value: _Optional[float] = ..., retained_order: bool = ..., sent_to_exchange: bool = ...) -> None: ...

class OrdersHistory(_message.Message):
    __slots__ = ["response_datetime", "values"]
    class Request(_message.Message):
        __slots__ = ["from_date", "to_date"]
        class Date(_message.Message):
            __slots__ = ["day", "month", "year"]
            DAY_FIELD_NUMBER: _ClassVar[int]
            MONTH_FIELD_NUMBER: _ClassVar[int]
            YEAR_FIELD_NUMBER: _ClassVar[int]
            day: int
            month: int
            year: int
            def __init__(self, year: _Optional[int] = ..., month: _Optional[int] = ..., day: _Optional[int] = ...) -> None: ...
        FROM_DATE_FIELD_NUMBER: _ClassVar[int]
        TO_DATE_FIELD_NUMBER: _ClassVar[int]
        from_date: OrdersHistory.Request.Date
        to_date: OrdersHistory.Request.Date
        def __init__(self, from_date: _Optional[_Union[OrdersHistory.Request.Date, _Mapping]] = ..., to_date: _Optional[_Union[OrdersHistory.Request.Date, _Mapping]] = ...) -> None: ...
    RESPONSE_DATETIME_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    response_datetime: _timestamp_pb2.Timestamp
    values: _containers.RepeatedCompositeFieldContainer[_struct_pb2.Struct]
    def __init__(self, values: _Optional[_Iterable[_Union[_struct_pb2.Struct, _Mapping]]] = ..., response_datetime: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class PositionReport(_message.Message):
    __slots__ = ["content", "format", "response_datetime"]
    class Format(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class Request(_message.Message):
        __slots__ = ["country", "format", "lang", "to_date"]
        class Date(_message.Message):
            __slots__ = ["day", "month", "year"]
            DAY_FIELD_NUMBER: _ClassVar[int]
            MONTH_FIELD_NUMBER: _ClassVar[int]
            YEAR_FIELD_NUMBER: _ClassVar[int]
            day: int
            month: int
            year: int
            def __init__(self, year: _Optional[int] = ..., month: _Optional[int] = ..., day: _Optional[int] = ...) -> None: ...
        COUNTRY_FIELD_NUMBER: _ClassVar[int]
        FORMAT_FIELD_NUMBER: _ClassVar[int]
        LANG_FIELD_NUMBER: _ClassVar[int]
        TO_DATE_FIELD_NUMBER: _ClassVar[int]
        country: str
        format: PositionReport.Format
        lang: str
        to_date: PositionReport.Request.Date
        def __init__(self, format: _Optional[_Union[PositionReport.Format, str]] = ..., country: _Optional[str] = ..., lang: _Optional[str] = ..., to_date: _Optional[_Union[PositionReport.Request.Date, _Mapping]] = ...) -> None: ...
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    CSV: PositionReport.Format
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    HTML: PositionReport.Format
    PDF: PositionReport.Format
    RESPONSE_DATETIME_FIELD_NUMBER: _ClassVar[int]
    XLS: PositionReport.Format
    content: str
    format: PositionReport.Format
    response_datetime: _timestamp_pb2.Timestamp
    def __init__(self, content: _Optional[str] = ..., format: _Optional[_Union[PositionReport.Format, str]] = ..., response_datetime: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ProductSearch(_message.Message):
    __slots__ = ["offset", "products", "response_datetime", "total"]
    class Config(_message.Message):
        __slots__ = ["values"]
        VALUES_FIELD_NUMBER: _ClassVar[int]
        values: _struct_pb2.Struct
        def __init__(self, values: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...
    class RequestBonds(_message.Message):
        __slots__ = ["bond_exchange_id", "bond_issuer_type_id", "limit", "offset", "require_total", "search_text", "sort_columns", "sort_types"]
        BOND_EXCHANGE_ID_FIELD_NUMBER: _ClassVar[int]
        BOND_ISSUER_TYPE_ID_FIELD_NUMBER: _ClassVar[int]
        LIMIT_FIELD_NUMBER: _ClassVar[int]
        OFFSET_FIELD_NUMBER: _ClassVar[int]
        REQUIRE_TOTAL_FIELD_NUMBER: _ClassVar[int]
        SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
        SORT_COLUMNS_FIELD_NUMBER: _ClassVar[int]
        SORT_TYPES_FIELD_NUMBER: _ClassVar[int]
        bond_exchange_id: int
        bond_issuer_type_id: int
        limit: int
        offset: int
        require_total: bool
        search_text: str
        sort_columns: str
        sort_types: str
        def __init__(self, bond_issuer_type_id: _Optional[int] = ..., bond_exchange_id: _Optional[int] = ..., search_text: _Optional[str] = ..., offset: _Optional[int] = ..., limit: _Optional[int] = ..., require_total: bool = ..., sort_columns: _Optional[str] = ..., sort_types: _Optional[str] = ...) -> None: ...
    class RequestETFs(_message.Message):
        __slots__ = ["input_aggregate_types", "input_aggregate_values", "limit", "offset", "popular_only", "require_total", "search_text", "sort_columns", "sort_types"]
        INPUT_AGGREGATE_TYPES_FIELD_NUMBER: _ClassVar[int]
        INPUT_AGGREGATE_VALUES_FIELD_NUMBER: _ClassVar[int]
        LIMIT_FIELD_NUMBER: _ClassVar[int]
        OFFSET_FIELD_NUMBER: _ClassVar[int]
        POPULAR_ONLY_FIELD_NUMBER: _ClassVar[int]
        REQUIRE_TOTAL_FIELD_NUMBER: _ClassVar[int]
        SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
        SORT_COLUMNS_FIELD_NUMBER: _ClassVar[int]
        SORT_TYPES_FIELD_NUMBER: _ClassVar[int]
        input_aggregate_types: str
        input_aggregate_values: str
        limit: int
        offset: int
        popular_only: bool
        require_total: bool
        search_text: str
        sort_columns: str
        sort_types: str
        def __init__(self, popular_only: bool = ..., input_aggregate_types: _Optional[str] = ..., input_aggregate_values: _Optional[str] = ..., search_text: _Optional[str] = ..., offset: _Optional[int] = ..., limit: _Optional[int] = ..., require_total: bool = ..., sort_columns: _Optional[str] = ..., sort_types: _Optional[str] = ...) -> None: ...
    class RequestFunds(_message.Message):
        __slots__ = ["limit", "offset", "require_total", "search_text", "sort_columns", "sort_types"]
        LIMIT_FIELD_NUMBER: _ClassVar[int]
        OFFSET_FIELD_NUMBER: _ClassVar[int]
        REQUIRE_TOTAL_FIELD_NUMBER: _ClassVar[int]
        SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
        SORT_COLUMNS_FIELD_NUMBER: _ClassVar[int]
        SORT_TYPES_FIELD_NUMBER: _ClassVar[int]
        limit: int
        offset: int
        require_total: bool
        search_text: str
        sort_columns: str
        sort_types: str
        def __init__(self, search_text: _Optional[str] = ..., offset: _Optional[int] = ..., limit: _Optional[int] = ..., require_total: bool = ..., sort_columns: _Optional[str] = ..., sort_types: _Optional[str] = ...) -> None: ...
    class RequestFutures(_message.Message):
        __slots__ = ["future_exchange_id", "limit", "offset", "require_total", "search_text", "sort_columns", "sort_types", "underlying_isin"]
        FUTURE_EXCHANGE_ID_FIELD_NUMBER: _ClassVar[int]
        LIMIT_FIELD_NUMBER: _ClassVar[int]
        OFFSET_FIELD_NUMBER: _ClassVar[int]
        REQUIRE_TOTAL_FIELD_NUMBER: _ClassVar[int]
        SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
        SORT_COLUMNS_FIELD_NUMBER: _ClassVar[int]
        SORT_TYPES_FIELD_NUMBER: _ClassVar[int]
        UNDERLYING_ISIN_FIELD_NUMBER: _ClassVar[int]
        future_exchange_id: int
        limit: int
        offset: int
        require_total: bool
        search_text: str
        sort_columns: str
        sort_types: str
        underlying_isin: str
        def __init__(self, future_exchange_id: _Optional[int] = ..., underlying_isin: _Optional[str] = ..., search_text: _Optional[str] = ..., offset: _Optional[int] = ..., limit: _Optional[int] = ..., require_total: bool = ..., sort_columns: _Optional[str] = ..., sort_types: _Optional[str] = ...) -> None: ...
    class RequestLeverageds(_message.Message):
        __slots__ = ["input_aggregate_types", "input_aggregate_values", "limit", "offset", "popular_only", "require_total", "search_text", "sort_columns", "sort_types"]
        INPUT_AGGREGATE_TYPES_FIELD_NUMBER: _ClassVar[int]
        INPUT_AGGREGATE_VALUES_FIELD_NUMBER: _ClassVar[int]
        LIMIT_FIELD_NUMBER: _ClassVar[int]
        OFFSET_FIELD_NUMBER: _ClassVar[int]
        POPULAR_ONLY_FIELD_NUMBER: _ClassVar[int]
        REQUIRE_TOTAL_FIELD_NUMBER: _ClassVar[int]
        SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
        SORT_COLUMNS_FIELD_NUMBER: _ClassVar[int]
        SORT_TYPES_FIELD_NUMBER: _ClassVar[int]
        input_aggregate_types: str
        input_aggregate_values: str
        limit: int
        offset: int
        popular_only: bool
        require_total: bool
        search_text: str
        sort_columns: str
        sort_types: str
        def __init__(self, popular_only: bool = ..., input_aggregate_types: _Optional[str] = ..., input_aggregate_values: _Optional[str] = ..., search_text: _Optional[str] = ..., offset: _Optional[int] = ..., limit: _Optional[int] = ..., require_total: bool = ..., sort_columns: _Optional[str] = ..., sort_types: _Optional[str] = ...) -> None: ...
    class RequestLookup(_message.Message):
        __slots__ = ["limit", "offset", "product_type_id", "search_text"]
        LIMIT_FIELD_NUMBER: _ClassVar[int]
        OFFSET_FIELD_NUMBER: _ClassVar[int]
        PRODUCT_TYPE_ID_FIELD_NUMBER: _ClassVar[int]
        SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
        limit: int
        offset: int
        product_type_id: int
        search_text: str
        def __init__(self, search_text: _Optional[str] = ..., limit: _Optional[int] = ..., offset: _Optional[int] = ..., product_type_id: _Optional[int] = ...) -> None: ...
    class RequestOptions(_message.Message):
        __slots__ = ["input_aggregate_types", "input_aggregate_values", "limit", "offset", "option_exchange_id", "require_total", "search_text", "sort_columns", "sort_types", "underlying_isin"]
        INPUT_AGGREGATE_TYPES_FIELD_NUMBER: _ClassVar[int]
        INPUT_AGGREGATE_VALUES_FIELD_NUMBER: _ClassVar[int]
        LIMIT_FIELD_NUMBER: _ClassVar[int]
        OFFSET_FIELD_NUMBER: _ClassVar[int]
        OPTION_EXCHANGE_ID_FIELD_NUMBER: _ClassVar[int]
        REQUIRE_TOTAL_FIELD_NUMBER: _ClassVar[int]
        SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
        SORT_COLUMNS_FIELD_NUMBER: _ClassVar[int]
        SORT_TYPES_FIELD_NUMBER: _ClassVar[int]
        UNDERLYING_ISIN_FIELD_NUMBER: _ClassVar[int]
        input_aggregate_types: str
        input_aggregate_values: str
        limit: int
        offset: int
        option_exchange_id: int
        require_total: bool
        search_text: str
        sort_columns: str
        sort_types: str
        underlying_isin: str
        def __init__(self, input_aggregate_types: _Optional[str] = ..., input_aggregate_values: _Optional[str] = ..., option_exchange_id: _Optional[int] = ..., underlying_isin: _Optional[str] = ..., search_text: _Optional[str] = ..., offset: _Optional[int] = ..., limit: _Optional[int] = ..., require_total: bool = ..., sort_columns: _Optional[str] = ..., sort_types: _Optional[str] = ...) -> None: ...
    class RequestStocks(_message.Message):
        __slots__ = ["exchange_id", "index_id", "is_in_us_green_list", "limit", "offset", "require_total", "search_text", "sort_columns", "sort_types", "stock_country_id"]
        EXCHANGE_ID_FIELD_NUMBER: _ClassVar[int]
        INDEX_ID_FIELD_NUMBER: _ClassVar[int]
        IS_IN_US_GREEN_LIST_FIELD_NUMBER: _ClassVar[int]
        LIMIT_FIELD_NUMBER: _ClassVar[int]
        OFFSET_FIELD_NUMBER: _ClassVar[int]
        REQUIRE_TOTAL_FIELD_NUMBER: _ClassVar[int]
        SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
        SORT_COLUMNS_FIELD_NUMBER: _ClassVar[int]
        SORT_TYPES_FIELD_NUMBER: _ClassVar[int]
        STOCK_COUNTRY_ID_FIELD_NUMBER: _ClassVar[int]
        exchange_id: int
        index_id: int
        is_in_us_green_list: bool
        limit: int
        offset: int
        require_total: bool
        search_text: str
        sort_columns: str
        sort_types: str
        stock_country_id: int
        def __init__(self, is_in_us_green_list: bool = ..., index_id: _Optional[int] = ..., exchange_id: _Optional[int] = ..., stock_country_id: _Optional[int] = ..., search_text: _Optional[str] = ..., offset: _Optional[int] = ..., limit: _Optional[int] = ..., require_total: bool = ..., sort_columns: _Optional[str] = ..., sort_types: _Optional[str] = ...) -> None: ...
    class RequestWarrants(_message.Message):
        __slots__ = ["limit", "offset", "require_total", "search_text", "sort_columns", "sort_types"]
        LIMIT_FIELD_NUMBER: _ClassVar[int]
        OFFSET_FIELD_NUMBER: _ClassVar[int]
        REQUIRE_TOTAL_FIELD_NUMBER: _ClassVar[int]
        SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
        SORT_COLUMNS_FIELD_NUMBER: _ClassVar[int]
        SORT_TYPES_FIELD_NUMBER: _ClassVar[int]
        limit: int
        offset: int
        require_total: bool
        search_text: str
        sort_columns: str
        sort_types: str
        def __init__(self, search_text: _Optional[str] = ..., offset: _Optional[int] = ..., limit: _Optional[int] = ..., require_total: bool = ..., sort_columns: _Optional[str] = ..., sort_types: _Optional[str] = ...) -> None: ...
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    PRODUCTS_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_DATETIME_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    offset: int
    products: _containers.RepeatedCompositeFieldContainer[_struct_pb2.Struct]
    response_datetime: _timestamp_pb2.Timestamp
    total: int
    def __init__(self, offset: _Optional[int] = ..., products: _Optional[_Iterable[_Union[_struct_pb2.Struct, _Mapping]]] = ..., response_datetime: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., total: _Optional[int] = ...) -> None: ...

class ProductsInfo(_message.Message):
    __slots__ = ["values"]
    class Request(_message.Message):
        __slots__ = ["products"]
        PRODUCTS_FIELD_NUMBER: _ClassVar[int]
        products: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, products: _Optional[_Iterable[int]] = ...) -> None: ...
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _struct_pb2.Struct
    def __init__(self, values: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class TopNewsPreview(_message.Message):
    __slots__ = ["items", "offset", "total"]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[_struct_pb2.Struct]
    offset: int
    total: int
    def __init__(self, items: _Optional[_Iterable[_Union[_struct_pb2.Struct, _Mapping]]] = ..., offset: _Optional[int] = ..., total: _Optional[int] = ...) -> None: ...

class TransactionsHistory(_message.Message):
    __slots__ = ["response_datetime", "values"]
    class Request(_message.Message):
        __slots__ = ["from_date", "group_transactions_by_order", "to_date"]
        class Date(_message.Message):
            __slots__ = ["day", "month", "year"]
            DAY_FIELD_NUMBER: _ClassVar[int]
            MONTH_FIELD_NUMBER: _ClassVar[int]
            YEAR_FIELD_NUMBER: _ClassVar[int]
            day: int
            month: int
            year: int
            def __init__(self, year: _Optional[int] = ..., month: _Optional[int] = ..., day: _Optional[int] = ...) -> None: ...
        FROM_DATE_FIELD_NUMBER: _ClassVar[int]
        GROUP_TRANSACTIONS_BY_ORDER_FIELD_NUMBER: _ClassVar[int]
        TO_DATE_FIELD_NUMBER: _ClassVar[int]
        from_date: TransactionsHistory.Request.Date
        group_transactions_by_order: bool
        to_date: TransactionsHistory.Request.Date
        def __init__(self, from_date: _Optional[_Union[TransactionsHistory.Request.Date, _Mapping]] = ..., to_date: _Optional[_Union[TransactionsHistory.Request.Date, _Mapping]] = ..., group_transactions_by_order: bool = ...) -> None: ...
    RESPONSE_DATETIME_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    response_datetime: _timestamp_pb2.Timestamp
    values: _containers.RepeatedCompositeFieldContainer[_struct_pb2.Struct]
    def __init__(self, values: _Optional[_Iterable[_Union[_struct_pb2.Struct, _Mapping]]] = ..., response_datetime: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class Update(_message.Message):
    __slots__ = ["alerts", "cash_funds", "historical_orders", "orders", "portfolio", "response_datetime", "total_portfolio", "transactions"]
    class Option(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class Alerts(_message.Message):
        __slots__ = ["last_updated", "values"]
        LAST_UPDATED_FIELD_NUMBER: _ClassVar[int]
        VALUES_FIELD_NUMBER: _ClassVar[int]
        last_updated: int
        values: _struct_pb2.Struct
        def __init__(self, last_updated: _Optional[int] = ..., values: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...
    class CashFunds(_message.Message):
        __slots__ = ["last_updated", "values"]
        LAST_UPDATED_FIELD_NUMBER: _ClassVar[int]
        VALUES_FIELD_NUMBER: _ClassVar[int]
        last_updated: int
        values: _struct_pb2.Struct
        def __init__(self, last_updated: _Optional[int] = ..., values: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...
    class HistoricalOrders(_message.Message):
        __slots__ = ["last_updated", "values"]
        LAST_UPDATED_FIELD_NUMBER: _ClassVar[int]
        VALUES_FIELD_NUMBER: _ClassVar[int]
        last_updated: int
        values: _containers.RepeatedCompositeFieldContainer[Order]
        def __init__(self, last_updated: _Optional[int] = ..., values: _Optional[_Iterable[_Union[Order, _Mapping]]] = ...) -> None: ...
    class Orders(_message.Message):
        __slots__ = ["last_updated", "values"]
        LAST_UPDATED_FIELD_NUMBER: _ClassVar[int]
        VALUES_FIELD_NUMBER: _ClassVar[int]
        last_updated: int
        values: _containers.RepeatedCompositeFieldContainer[Order]
        def __init__(self, last_updated: _Optional[int] = ..., values: _Optional[_Iterable[_Union[Order, _Mapping]]] = ...) -> None: ...
    class Portfolio(_message.Message):
        __slots__ = ["last_updated", "values"]
        LAST_UPDATED_FIELD_NUMBER: _ClassVar[int]
        VALUES_FIELD_NUMBER: _ClassVar[int]
        last_updated: int
        values: _containers.RepeatedCompositeFieldContainer[_struct_pb2.Struct]
        def __init__(self, last_updated: _Optional[int] = ..., values: _Optional[_Iterable[_Union[_struct_pb2.Struct, _Mapping]]] = ...) -> None: ...
    class Request(_message.Message):
        __slots__ = ["last_updated", "option"]
        LAST_UPDATED_FIELD_NUMBER: _ClassVar[int]
        OPTION_FIELD_NUMBER: _ClassVar[int]
        last_updated: int
        option: Update.Option
        def __init__(self, option: _Optional[_Union[Update.Option, str]] = ..., last_updated: _Optional[int] = ...) -> None: ...
    class RequestList(_message.Message):
        __slots__ = ["values"]
        VALUES_FIELD_NUMBER: _ClassVar[int]
        values: _containers.RepeatedCompositeFieldContainer[Update.Request]
        def __init__(self, values: _Optional[_Iterable[_Union[Update.Request, _Mapping]]] = ...) -> None: ...
    class TotalPortfolio(_message.Message):
        __slots__ = ["last_updated", "values"]
        LAST_UPDATED_FIELD_NUMBER: _ClassVar[int]
        VALUES_FIELD_NUMBER: _ClassVar[int]
        last_updated: int
        values: _struct_pb2.Struct
        def __init__(self, last_updated: _Optional[int] = ..., values: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...
    class Transactions(_message.Message):
        __slots__ = ["last_updated", "values"]
        LAST_UPDATED_FIELD_NUMBER: _ClassVar[int]
        VALUES_FIELD_NUMBER: _ClassVar[int]
        last_updated: int
        values: _containers.RepeatedCompositeFieldContainer[_struct_pb2.Struct]
        def __init__(self, last_updated: _Optional[int] = ..., values: _Optional[_Iterable[_Union[_struct_pb2.Struct, _Mapping]]] = ...) -> None: ...
    ALERTS: Update.Option
    ALERTS_FIELD_NUMBER: _ClassVar[int]
    CASHFUNDS: Update.Option
    CASH_FUNDS_FIELD_NUMBER: _ClassVar[int]
    HISTORICALORDERS: Update.Option
    HISTORICAL_ORDERS_FIELD_NUMBER: _ClassVar[int]
    ORDERS: Update.Option
    ORDERS_FIELD_NUMBER: _ClassVar[int]
    PORTFOLIO: Update.Option
    PORTFOLIO_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_DATETIME_FIELD_NUMBER: _ClassVar[int]
    TOTALPORTFOLIO: Update.Option
    TOTAL_PORTFOLIO_FIELD_NUMBER: _ClassVar[int]
    TRANSACTIONS: Update.Option
    TRANSACTIONS_FIELD_NUMBER: _ClassVar[int]
    alerts: Update.Alerts
    cash_funds: Update.CashFunds
    historical_orders: Update.HistoricalOrders
    orders: Update.Orders
    portfolio: Update.Portfolio
    response_datetime: _timestamp_pb2.Timestamp
    total_portfolio: Update.TotalPortfolio
    transactions: Update.Transactions
    def __init__(self, response_datetime: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., alerts: _Optional[_Union[Update.Alerts, _Mapping]] = ..., cash_funds: _Optional[_Union[Update.CashFunds, _Mapping]] = ..., historical_orders: _Optional[_Union[Update.HistoricalOrders, _Mapping]] = ..., orders: _Optional[_Union[Update.Orders, _Mapping]] = ..., portfolio: _Optional[_Union[Update.Portfolio, _Mapping]] = ..., total_portfolio: _Optional[_Union[Update.TotalPortfolio, _Mapping]] = ..., transactions: _Optional[_Union[Update.Transactions, _Mapping]] = ...) -> None: ...
