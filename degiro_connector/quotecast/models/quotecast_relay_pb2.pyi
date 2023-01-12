from google.protobuf import wrappers_pb2 as _wrappers_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from degiro_connector.quotecast.models import quotecast_pb2 as _quotecast_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SetConfig(_message.Message):
    __slots__ = ["auto_connect", "user_token"]
    AUTO_CONNECT_FIELD_NUMBER: _ClassVar[int]
    USER_TOKEN_FIELD_NUMBER: _ClassVar[int]
    auto_connect: bool
    user_token: int
    def __init__(self, user_token: _Optional[int] = ..., auto_connect: bool = ...) -> None: ...
