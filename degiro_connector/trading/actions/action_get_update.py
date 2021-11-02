# IMPORTATION STANDARD
import requests
import logging
from typing import Dict, Union

# IMPORTATION THIRD PARTY

# IMPORTATION INTERNAL
import degiro_connector.core.constants.urls as urls
from degiro_connector.trading.models.trading_pb2 import (
    Credentials,
    Order,
    Update,
)
from degiro_connector.core.abstracts.abstract_action import AbstractAction


class ActionGetUpdate(AbstractAction):
    ACTION_MATCHING = {
        "B": Order.Action.Value("BUY"),
        "S": Order.Action.Value("SELL"),
    }
    ORDER_MATCHING = {
        "buysell": "action",
        "contractSize": "contract_size",
        "contractType": "contract_type",
        "currency": "currency",
        "date": "hour",
        "id": "id",
        "isDeletable": "is_deletable",
        "isModifiable": "is_modifiable",
        "orderTimeTypeId": "time_type",
        "orderTypeId": "order_type",
        "price": "price",
        "product": "product",
        "productId": "product_id",
        "quantity": "quantity",
        "size": "size",
        "stopPrice": "stop_price",
        "totalOrderValue": "total_order_value",
    }
    UPDATE_OPTION_MATCHING = {
        Update.Option.Value("ALERTS"): "alerts",
        Update.Option.Value("CASHFUNDS"): "cashFunds",
        Update.Option.Value("HISTORICALORDERS"): "historicalOrders",
        Update.Option.Value("ORDERS"): "orders",
        Update.Option.Value("PORTFOLIO"): "portfolio",
        Update.Option.Value("TOTALPORTFOLIO"): "totalPortfolio",
        Update.Option.Value("TRANSACTIONS"): "transactions",
    }

    @classmethod
    def update_request_list_to_api(cls, request_list: Update.RequestList) -> dict:
        """Makes a payload compatible with the API.
        Parameters:
            update_option_list {UpdateOptionList}
                List of option available from grpc "consume_update".
        Returns:
            {dict}
                Payload that Degiro's update endpoint can understand.
        """

        payload = dict()

        for request in request_list.values:
            option = cls.UPDATE_OPTION_MATCHING[request.option]
            payload[option] = request.last_updated

        return payload

    @classmethod
    def setup_update_orders(cls, update: Update, payload: dict):
        """Build an "Order" object using "dict" returned by the API.
        Parameters:
            order {dict}
                Order dict straight from Degiro's API
        Returns:
            {Order}
        """

        if "orders" in payload:
            update.orders.last_updated = payload["orders"]["lastUpdated"]

            for order in payload["orders"]["value"]:
                order_dict = dict()
                for attribute in order["value"]:
                    if (
                        "name" in attribute
                        and "value" in attribute
                        and attribute["name"] in cls.ORDER_MATCHING
                    ):
                        order_dict[cls.ORDER_MATCHING[attribute["name"]]] = attribute[
                            "value"
                        ]

                order_dict["action"] = cls.ACTION_MATCHING[order_dict["action"]]
                update.orders.values.append(Order(**order_dict))

    @classmethod
    def setup_update_portfolio(cls, update: Update, payload: dict):
        if "portfolio" in payload:
            update.portfolio.last_updated = payload["portfolio"]["lastUpdated"]

            for positionrow in payload["portfolio"]["value"]:
                value = update.portfolio.values.add()
                for attribute in positionrow["value"]:
                    if "name" in attribute and "value" in attribute:
                        value[attribute["name"]] = attribute["value"]

    @classmethod
    def setup_update_total_portfolio(cls, update: Update, payload: dict):
        if "totalPortfolio" in payload:
            update.total_portfolio.last_updated = payload["totalPortfolio"][
                "lastUpdated"
            ]

            for attribute in payload["totalPortfolio"]["value"]:
                if "name" in attribute and "value" in attribute:
                    name = attribute["name"]
                    value = attribute["value"]
                    update.total_portfolio.values[name] = value

    @classmethod
    def update_to_grpc(cls, payload: dict) -> Update:
        update = Update()
        update.response_datetime.GetCurrentTime()

        # ORDERS
        cls.setup_update_orders(update=update, payload=payload)

        # PORTFOLIO
        cls.setup_update_portfolio(
            update=update,
            payload=payload,
        )

        # TOTALPORTFOLIO
        cls.setup_update_total_portfolio(
            update=update,
            payload=payload,
        )

        return update

    @classmethod
    def get_update(
        cls,
        request_list: Update.RequestList,
        session_id: str,
        credentials: Credentials,
        logger: logging.Logger = None,
        raw: bool = False,
        session: requests.Session = None,
    ) -> Union[Update, Dict, None]:
        """Retrieve information from Degiro's Trading Update endpoint.
        Args:
            request (Update.RequestList):
                List of options that we want to retrieve from the endpoint.
                Example :
                    request = Update.RequestList()
                    request.list.extend(
                        [
                            Update.Request(
                                option=Update.Option.ALERTS,
                                last_updated=0,
                            ),
                            Update.Request(
                                option=Update.Option.CASHFUNDS,
                                last_updated=0,
                            ),
                            Update.Request(
                                option=Update.Option.HISTORICALORDERS,
                                last_updated=0,
                            ),
                            Update.Request(
                                option=Update.Option.ORDERS,
                                last_updated=0,
                            ),
                            Update.Request(
                                option=Update.Option.PORTFOLIO,
                                last_updated=0,
                            ),
                            Update.Request(
                                option=Update.Option.TOTALPORTFOLIO,
                                last_updated=0,
                            ),
                            Update.Request(
                                option=Update.Option.TRANSACTIONS,
                                last_updated=0,
                            ),
                        ]
                    )
            session_id (str):
                API's session id.
            credentials (Credentials):
                Credentials containing the parameter "int_account".
            raw (bool, optional):
                Whether are not we want the raw API response.
                Defaults to False.
            session (requests.Session, optional):
                This object will be generated if None.
                Defaults to None.
            logger (logging.Logger, optional):
                This object will be generated if None.
                Defaults to None.
        Returns:
            Update: API response.
        """

        if logger is None:
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        int_account = credentials.int_account
        url = urls.UPDATE
        url = f"{url}/{int_account};jsessionid={session_id}"

        params = cls.update_request_list_to_api(request_list=request_list)
        params["intAccount"] = int_account
        params["sessionId"] = session_id

        request = requests.Request(method="GET", url=url, params=params)
        prepped = session.prepare_request(request)
        response_raw = None

        try:
            response_raw = session.send(prepped, verify=False)
            response_raw.raise_for_status()
            response_dict = response_raw.json()

            if raw is True:
                return response_dict
            else:
                return cls.update_to_grpc(
                    payload=response_dict,
                )
        except Exception as e:
            logger.fatal("error")
            logger.fatal(response_raw)
            logger.fatal(e)
            return None

    def call(
        self,
        request_list: Update.RequestList,
        raw: bool = False,
    ) -> Union[Update, Dict, None]:
        credentials = self.credentials
        connection_storage = self.connection_storage
        session_id = connection_storage.session_id
        session = self.session_storage.session
        logger = self.logger

        return self.get_update(
            request_list=request_list,
            session_id=session_id,
            credentials=credentials,
            logger=logger,
            raw=raw,
            session=session,
        )
