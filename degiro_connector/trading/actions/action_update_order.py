# IMPORTATION STANDARD
import logging
from typing import Dict, Union

# IMPORTATION THIRD PARTY
import requests
from google.protobuf import json_format

# IMPORTATION INTERNAL
import degiro_connector.core.constants.urls as urls
from degiro_connector.core.abstracts.abstract_action import AbstractAction
from degiro_connector.trading.models.trading_pb2 import (
    Credentials,
    Order,
)


class ActionUpdateOrder(AbstractAction):
    ORDER_FILTER_MATCHING = {
        Order.OrderType.LIMIT: {
            "buySell",
            "orderType",
            "price",
            "productId",
            "size",
            "timeType",
        },
        Order.OrderType.STOP_LIMIT: {
            "buySell",
            "orderType",
            "price",
            "productId",
            "size",
            "stopPrice",
            "timeType",
        },
        Order.OrderType.MARKET: {
            "buySell",
            "orderType",
            "productId",
            "size",
            "timeType",
        },
        Order.OrderType.STOP_LOSS: {
            "buySell",
            "orderType",
            "productId",
            "size",
            "stopPrice",
            "timeType",
        },
    }

    @classmethod
    def order_to_api(cls, order: Order) -> Dict[str, Union[float, int, str]]:
        # Build dict from message
        order_dict = json_format.MessageToDict(
            message=order,
            including_default_value_fields=True,
            preserving_proto_field_name=False,
            use_integers_for_enums=True,
            descriptor_pool=None,
            float_precision=None,
        )

        # Setup 'buySell'
        if order.action == order.Action.BUY:
            order_dict["buySell"] = "BUY"
        else:
            order_dict["buySell"] = "SELL"

        # Filter fields
        fields_to_keep = set()
        if order.order_type in cls.ORDER_FILTER_MATCHING:
            fields_to_keep = cls.ORDER_FILTER_MATCHING[order.order_type]
        else:
            raise AttributeError("Invalid `OrderType`.")

        filtered_order_dict = dict()
        for field in order_dict.keys() & fields_to_keep:
            filtered_order_dict[field] = order_dict[field]

        return filtered_order_dict

    @classmethod
    def update_order(
        cls,
        order: Order,
        session_id: str,
        credentials: Credentials,
        session: requests.Session = None,
        logger: logging.Logger = None,
        raw: bool = False,
    ) -> Union[bool, None]:
        if logger is None:
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        int_account = credentials.int_account
        order_id = order.id
        url = urls.ORDER_UPDATE
        url = f"{url}/{order_id};jsessionid={session_id}"

        params = {
            "intAccount": int_account,
            "sessionId": session_id,
        }

        order_dict = cls.order_to_api(order=order)

        request = requests.Request(
            method="PUT",
            url=url,
            json=order_dict,
            params=params,
        )
        prepped = session.prepare_request(request)
        response_raw = None

        try:
            response_raw = session.send(prepped, verify=False)
            response_raw.raise_for_status()
        except requests.HTTPError as e:
            status_code = getattr(response_raw, "status_code", "No status_code found.")
            text = getattr(response_raw, "text", "No text found.")
            logger.fatal(status_code)
            logger.fatal(text)
            if raw is True:
                response_dict = response_raw.json()
                return response_dict
            return None
        except Exception as e:
            logger.fatal(e)
            return None

        return response_raw.status_code == 200

    def call(
        self,
        order: Order,
        raw: bool = False,
    ) -> Union[bool, None]:
        connection_storage = self.connection_storage
        session_id = connection_storage.session_id
        session = self.session_storage.session
        credentials = self.credentials
        logger = self.logger

        return self.update_order(
            order=order,
            session_id=session_id,
            credentials=credentials,
            session=session,
            logger=logger,
            raw=raw,
        )
