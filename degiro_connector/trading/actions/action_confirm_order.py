import logging
import time
from datetime import datetime, timedelta

import requests
from orjson import loads

from degiro_connector.core.constants import urls
from degiro_connector.trading.models.credentials import Credentials
from degiro_connector.trading.models.order import (
    ConfirmationResponse,
    ConfirmationWrapper,
    Order,
    ORDER_FIELD_MAP,
)
from degiro_connector.core.abstracts.abstract_action import AbstractAction


class ActionConfirmOrder(AbstractAction):
    @staticmethod
    def build_json_map(order: Order) -> dict[str, float | int | str]:
        json_map = order.model_dump(
            by_alias=True,
            exclude_none=True,
            mode="json",
        )

        if order.order_type not in ORDER_FIELD_MAP:
            raise AttributeError("Invalid `OrderType`.")

        if order.buy_sell is None:
            raise AttributeError("Invalid `buy_sell`.")

        field_list = ORDER_FIELD_MAP[order.order_type]
        json_map = {field: json_map[field] for field in field_list if field in json_map}

        return json_map

    @staticmethod
    def build_model(
        response: requests.Response,
        duration_ns: int,
    ) -> ConfirmationResponse:
        model = ConfirmationWrapper.model_validate_json(json_data=response.text).data
        model.response_datetime = datetime.now()
        model.request_duration = timedelta(microseconds=duration_ns // 1000)

        return model

    @classmethod
    def confirm_order(
        cls,
        confirmation_id: str,
        credentials: Credentials,
        order: Order,
        session_id: str,
        logger: logging.Logger | None = None,
        raw: bool = False,
        session: requests.Session | None = None,
    ) -> ConfirmationResponse | dict | None:
        if logger is None:
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        int_account = credentials.int_account
        url = urls.ORDER_CONFIRM
        url = f"{url}/{confirmation_id};jsessionid={session_id}"
        params = {"intAccount": int_account, "sessionId": session_id}
        json_map = cls.build_json_map(order=order)
        request = requests.Request(
            method="POST",
            url=url,
            json=json_map,
            params=params,
        )
        prepped = session.prepare_request(request)
        start_ns = time.perf_counter_ns()

        try:
            response = session.send(prepped)
            duration_ns = time.perf_counter_ns() - start_ns
            response.raise_for_status()

            if raw is True:
                model = loads(response.text)
            else:
                model = cls.build_model(
                    response=response,
                    duration_ns=duration_ns,
                )
            return model
        except requests.HTTPError as e:
            logger.fatal(e)
            if isinstance(e.response, requests.Response):
                logger.fatal(e.response.text)
            if raw is True:
                model = loads(response.text)
                return model
            else:
                return None
        except Exception as e:
            logger.fatal(e)
            return None

    def call(
        self,
        confirmation_id: str,
        order: Order,
        raw: bool = False,
    ) -> ConfirmationResponse | dict | None:
        connection_storage = self.connection_storage
        session_id = connection_storage.session_id
        credentials = self.credentials
        session = self.session_storage.session
        logger = self.logger

        return self.confirm_order(
            confirmation_id=confirmation_id,
            credentials=credentials,
            order=order,
            session_id=session_id,
            logger=logger,
            raw=raw,
            session=session,
        )
