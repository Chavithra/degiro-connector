import logging

import requests

from degiro_connector.core.constants import urls
from degiro_connector.core.abstracts.abstract_action import AbstractAction
from degiro_connector.trading.models.credentials import Credentials
from degiro_connector.trading.models.order import Order, ORDER_FIELD_MAP


class ActionUpdateOrder(AbstractAction):
    @staticmethod
    def build_json_map(order: Order) -> dict:
        json_map = order.model_dump(
            by_alias=True,
            exclude_none=True,
            mode="json",
        )

        if order.id is None:
            raise AttributeError("No `order.id` provided.")

        if order.order_type not in ORDER_FIELD_MAP:
            raise AttributeError("Invalid `OrderType`.")

        if order.buy_sell is None:
            raise AttributeError("Invalid `buy_sell`.")

        field_list = ORDER_FIELD_MAP[order.order_type]
        json_map = {field: json_map[field] for field in field_list if field in json_map}

        return json_map

    @classmethod
    def update_order(
        cls,
        order: Order,
        session_id: str,
        credentials: Credentials,
        session: requests.Session | None = None,
        logger: logging.Logger | None = None,
    ) -> bool | None:
        if logger is None:
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        int_account = credentials.int_account
        order_id = order.id
        url = urls.ORDER_UPDATE
        url = f"{url}/{order_id};jsessionid={session_id}"
        params = {"intAccount": int_account, "sessionId": session_id}
        json_map = cls.build_json_map(order=order)
        request = requests.Request(
            method="PUT",
            url=url,
            json=json_map,
            params=params,
        )
        prepped = session.prepare_request(request)
        response_raw = None

        try:
            response_raw = session.send(prepped)
            response_raw.raise_for_status()

            return response_raw.status_code == 200
        except requests.HTTPError as e:
            logger.fatal(e)
            if isinstance(e.response, requests.Response):
                logger.fatal(e.response.text)
            return None
        except Exception as e:
            logger.fatal(e)
            return None

    def call(
        self,
        order: Order,
    ) -> bool | None:
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
        )
