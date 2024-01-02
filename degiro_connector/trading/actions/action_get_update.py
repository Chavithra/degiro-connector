import logging

import requests
from orjson import loads

from degiro_connector.core.constants import urls
from degiro_connector.trading.models.credentials import Credentials
from degiro_connector.trading.models.account import AccountUpdate, UpdateRequest
from degiro_connector.core.abstracts.abstract_action import AbstractAction


class ActionGetUpdate(AbstractAction):
    # ACTION_MATCHING = {
    #     "B": Order.Action.Value("BUY"),
    #     "S": Order.Action.Value("SELL"),
    # }
    # ORDER_MATCHING = {
    #     "buysell": "action",
    #     "contractSize": "contract_size",
    #     "contractType": "contract_type",
    #     "currency": "currency",
    #     "date": "hour",
    #     "id": "id",
    #     "isDeletable": "is_deletable",
    #     "isModifiable": "is_modifiable",
    #     "orderTimeTypeId": "time_type",
    #     "orderTypeId": "order_type",
    #     "price": "price",
    #     "product": "product",
    #     "productId": "product_id",
    #     "quantity": "quantity",
    #     "size": "size",
    #     "stopPrice": "stop_price",
    #     "totalOrderValue": "total_order_value",
    # }

    @staticmethod
    def build_model(response: requests.Response) -> AccountUpdate:
        model = AccountUpdate.model_validate_json(json_data=response.text)

        return model

    @staticmethod
    def build_params_map(request_list: list[UpdateRequest]) -> dict:
        params_map = {}

        for update_request in request_list:
            params_map[update_request.option.value] = update_request.last_updated

        return params_map

    @classmethod
    def get_update(
        cls,
        request_list: list[UpdateRequest],
        session_id: str,
        credentials: Credentials,
        logger: logging.Logger | None = None,
        raw: bool = False,
        session: requests.Session | None = None,
    ) -> AccountUpdate | dict | None:
        """Retrieve information from Degiro's Trading Update endpoint.
        Args:
            request_list (list[UpdateRequest]):
                list of options that we want to retrieve from the endpoint.
                Example :
                    request_list = [
                        UpdateRequest(
                            option=UpdateOption.ALERTS,
                            last_updated=0,
                        ),
                        UpdateRequest(
                            option=UpdateOption.CASH_FUNDS,
                            last_updated=0,
                        ),
                        UpdateRequest(
                            option=UpdateOption.HISTORICAL_ORDERS,
                            last_updated=0,
                        ),
                        UpdateRequest(
                            option=UpdateOption.ORDERS,
                            last_updated=0,
                        ),
                        UpdateRequest(
                            option=UpdateOption.PORTFOLIO,
                            last_updated=0,
                        ),
                        UpdateRequest(
                            option=UpdateOption.TOTAL_PORTFOLIO,
                            last_updated=0,
                        ),
                        UpdateRequest(
                            option=UpdateOption.TRANSACTIONS,
                            last_updated=0,
                        ),
                    ]
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
        params_map = cls.build_params_map(request_list=request_list)
        params_map.update({"intAccount": int_account, "sessionId": session_id})

        request = requests.Request(
            method="GET",
            params=params_map,
            url=url,
        )
        prepped = session.prepare_request(request)

        try:
            response = session.send(prepped)
            response.raise_for_status()

            if raw is True:
                model = loads(response.text)
            else:
                model = cls.build_model(response=response)
            return model
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
        request_list: list[UpdateRequest],
        raw: bool = False,
    ) -> AccountUpdate | dict | None:
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
