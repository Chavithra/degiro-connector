# IMPORTATION STANDARD
# IMPORTATION THIRD PARTY
# IMPORTATION INTERNAL
from google.protobuf import json_format
from google.protobuf.message import Message


def message_to_dict(message: Message) -> dict:
    return json_format.MessageToDict(
        message=message,
        including_default_value_fields=True,
        preserving_proto_field_name=True,
        use_integers_for_enums=True,
        descriptor_pool=None,
        float_precision=None,
    )
