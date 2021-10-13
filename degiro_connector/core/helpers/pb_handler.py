# IMPORTATION STANDARD

# IMPORTATION THIRD PARTY
from google.protobuf import json_format
from google.protobuf.message import Message
from google.protobuf.struct_pb2 import Struct

# IMPORTATION INTERNAL


def message_to_dict(message: Message) -> dict:
    return json_format.MessageToDict(
        message=message,
        including_default_value_fields=True,
        preserving_proto_field_name=True,
        use_integers_for_enums=True,
        descriptor_pool=None,
        float_precision=None,
    )


def struct_from_dict(json_dict: dict) -> Struct:
    return json_format.ParseDict(
        js_dict=json_dict,
        message=Struct(),
        ignore_unknown_fields=True,
        descriptor_pool=None,
    )
