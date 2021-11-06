# IMPORTATION STANDARD
from concurrent import futures
from functools import wraps
from typing import Any, Callable, List, Optional

# IMPORTATION THIRD PARTY
import grpc
from degiro_connector.trading.actions.action_connect import ActionConnect
from google.protobuf import json_format
from google.protobuf.empty_pb2 import Empty
from google.protobuf.struct_pb2 import Struct
from google.protobuf.wrappers_pb2 import (
    BoolValue,
    DoubleValue,
    Int64Value,
    StringValue,
)

# IMPORTATION INTERNAL
from degiro_connector.trading.api import API
from degiro_connector.trading.models.trading_pb2 import Credentials
from degiro_connector.trading.models.trading_relay_pb2_grpc import (
    add_TradingRelayServicer_to_server,
    TradingRelayServicer,
)


class Relay(TradingRelayServicer):
    OVERRIDED_METHOD_LIST = [
        "confirm_order",
        "product_search",
    ]
    PB_WRAPPERS_PATH = "google/protobuf/wrappers.proto"
    PY_TO_PB_TABLE = {
        bool: BoolValue,
        dict: Struct,
        int: Int64Value,
        float: DoubleValue,
        str: StringValue,
    }

    @classmethod
    def get_service_list(cls):
        service_list = list()

        for attr in dir(cls.__bases__[0]):
            if attr[:2] != "__":
                service_list.append(attr)
        return service_list

    @classmethod
    def pb_to_py(cls, obj) -> Optional[Any]:
        if isinstance(obj, Empty):
            return None
        elif obj.DESCRIPTOR.file.name == cls.PB_WRAPPERS_PATH:
            return obj.value
        else:
            return obj

    @classmethod
    def py_to_pb(cls, obj):
        obj_type = type(obj)
        if obj is None:
            return Empty()
        elif obj_type in cls.PY_TO_PB_TABLE:
            return json_format.ParseDict(
                js_dict=obj,
                message=cls.PY_TO_PB_TABLE[obj_type](),
                ignore_unknown_fields=True,
                descriptor_pool=None,
            )
        else:
            return obj

    def build_service_func(self, action_func: Callable) -> Callable:
        @wraps(action_func)
        def service_func(request, context):
            print("REQUEST : action_func", action_func)
            # print("REQUEST : request", request)
            print("REQUEST : request type", type(request))
            # print("REQUEST: context", context)

            is_action_connect = isinstance(action_func, ActionConnect)
            print("REQUEST : is_action_connect", is_action_connect)
            if not is_action_connect and self.auto_connect:
                connection_storage = self.api.connection_storage
                is_timeout_expired = connection_storage.is_timeout_expired()
                is_connected = connection_storage.connected.is_set()

                # print("REQUEST : self type", type(connection_storage))
                print("REQUEST : is_timeout_expired", is_timeout_expired)
                print("REQUEST : is_connected", is_connected)

                if not is_connected or is_timeout_expired:
                    self.api.connect()

            request_py = self.pb_to_py(obj=request)
            # print("INPUT PY : request_py", request_py)
            print("REQUEST : request_py type", type(request_py))
            if request_py is None:
                response = action_func()
            else:
                response = action_func(request_py)
            response_pb = self.py_to_pb(obj=response)
            # print("RESPONSE", response_pb)
            print("RESPONSE : type", type(response_pb))
            return response_pb

        return service_func

    @property
    def api(self):
        return self._api

    @property
    def auto_connect(self):
        return self._auto_connect

    def __init__(self, auto_connect: bool = False, credentials: Credentials = None):
        self._api = API(credentials=credentials or Credentials())
        self._auto_connect = auto_connect
        self._service_list = self.get_service_list()
        self.load_service_list(service_list=self._service_list)

    def load_service(self, service: str):
        action_list = self._api.action_list

        if service in action_list and not service in self.OVERRIDED_METHOD_LIST:
            print(service)
            action_func = getattr(self._api, service)
            service_func = self.build_service_func(action_func=action_func)
            setattr(self, service, service_func)

    def load_service_list(self, service_list: List[str]):
        for service in service_list:
            self.load_service(service=service)

    def serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        add_TradingRelayServicer_to_server(self, server)
        server.add_insecure_port("[::]:50051")
        server.start()

        print("STARTING :", self.__class__)

        try:
            server.wait_for_termination()
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            server.stop(grace=0)

    def set_config(self, request, context):
        print("REQUEST :", request)
        credentials = request.credentials
        auto_connect = request.auto_connect
        self._api.credentials.CopyFrom(credentials)
        self._auto_connect = auto_connect

        print("RESPONSE :", True)
        return BoolValue(value=True)

    def confirm_order(self, request, context):
        print("REQUEST :", request)
        confirmation_id = request.confirmation_id
        order = request.order
        confirmation_response = self._api.confirm_order(
            confirmation_id=confirmation_id,
            order=order,
            raw=False,
        )

        print("RESPONSE :", confirmation_response)
        return confirmation_response

    def product_search(self, request, context):
        print("REQUEST :", request)

        oneof = request.WhichOneof("request")
        product_search_request = getattr(request, oneof)
        product_search = self._api.product_search(
            request=product_search_request,
            raw=False,
        )

        print("RESPONSE :", product_search)
        return product_search
