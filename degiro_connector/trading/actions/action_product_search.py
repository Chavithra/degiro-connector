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
    ProductSearch,
)


class ActionProductSearch(AbstractAction):
    PRODUCT_SEARCH_REQUEST_URL_MATCHING = {
        ProductSearch.RequestBonds.DESCRIPTOR.full_name: urls.PRODUCT_SEARCH_BONDS,
        ProductSearch.RequestETFs.DESCRIPTOR.full_name: urls.PRODUCT_SEARCH_ETFS,
        ProductSearch.RequestFunds.DESCRIPTOR.full_name: urls.PRODUCT_SEARCH_FUNDS,
        ProductSearch.RequestFutures.DESCRIPTOR.full_name: urls.PRODUCT_SEARCH_FUTURES,
        ProductSearch.RequestLeverageds.DESCRIPTOR.full_name: urls.PRODUCT_SEARCH_LEVERAGEDS,
        ProductSearch.RequestLookup.DESCRIPTOR.full_name: urls.PRODUCT_SEARCH_LOOKUP,
        ProductSearch.RequestOptions.DESCRIPTOR.full_name: urls.PRODUCT_SEARCH_OPTIONS,
        ProductSearch.RequestStocks.DESCRIPTOR.full_name: urls.PRODUCT_SEARCH_STOCKS,
        ProductSearch.RequestWarrants.DESCRIPTOR.full_name: urls.PRODUCT_SEARCH_WARRANTS,
    }

    @staticmethod
    def product_search_request_to_api(
        request: Union[
            ProductSearch.RequestBonds,
            ProductSearch.RequestETFs,
            ProductSearch.RequestFunds,
            ProductSearch.RequestFutures,
            ProductSearch.RequestLeverageds,
            ProductSearch.RequestLookup,
            ProductSearch.RequestOptions,
            ProductSearch.RequestStocks,
            ProductSearch.RequestWarrants,
        ],
    ) -> dict:
        request_dict = json_format.MessageToDict(
            message=request,
            including_default_value_fields=False,
            preserving_proto_field_name=False,
            use_integers_for_enums=True,
            descriptor_pool=None,
            float_precision=None,
        )

        return request_dict

    @staticmethod
    def product_search_to_grpc(payload: dict) -> ProductSearch:
        product_search = ProductSearch()
        product_search.response_datetime.GetCurrentTime()
        json_format.ParseDict(
            js_dict=payload,
            message=product_search,
            ignore_unknown_fields=True,
            descriptor_pool=None,
        )

        return product_search

    @classmethod
    def product_search(
        cls,
        request: Union[
            ProductSearch.RequestBonds,
            ProductSearch.RequestETFs,
            ProductSearch.RequestFunds,
            ProductSearch.RequestFutures,
            ProductSearch.RequestLeverageds,
            ProductSearch.RequestLookup,
            ProductSearch.RequestOptions,
            ProductSearch.RequestStocks,
            ProductSearch.RequestWarrants,
        ],
        session_id: str,
        credentials: Credentials,
        raw: bool = False,
        session: requests.Session = None,
        logger: logging.Logger = None,
    ) -> Union[ProductSearch, Dict, None]:
        """Search products.
        Args:
            request (StockList.Request):
                List of options that we want to retrieve from the endpoint.
                Example 1:
                    request = ProductSearch.RequestLookup(
                        search_text='APPLE',
                        limit=10,
                        offset=0,
                    )
                Example 2:
                    request = ProductSearch.RequestStocks(
                        index_id=5,
                        is_in_us_green_list=False,
                        stock_country_id=886,
                        offset=0,
                        limit=100,
                        require_total=True,
                        sort_columns='name',
                        sort_types='asc',
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
            ProductSearch: API response.
        """

        if logger is None:
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        url = cls.PRODUCT_SEARCH_REQUEST_URL_MATCHING[request.DESCRIPTOR.full_name]

        params = cls.product_search_request_to_api(
            request=request,
        )

        if credentials.int_account > 0:
            params["intAccount"] = credentials.int_account

        params["sessionId"] = session_id

        http_request = requests.Request(method="GET", url=url, params=params)
        prepped = session.prepare_request(http_request)
        response_raw = None

        try:
            response_raw = session.send(prepped, verify=False)
            response_raw.raise_for_status()
            response_dict = response_raw.json()

            if raw is True:
                return response_dict
            else:
                return cls.product_search_to_grpc(
                    payload=response_dict,
                )
        except requests.HTTPError as e:
            status_code = getattr(response_raw, "status_code", "No status_code found.")
            text = getattr(response_raw, "text", "No text found.")
            logger.fatal(status_code)
            logger.fatal(text)
            return None
        except Exception as e:
            logger.fatal(e)
            return None

    def call(
        self,
        request: Union[
            ProductSearch.RequestBonds,
            ProductSearch.RequestETFs,
            ProductSearch.RequestFunds,
            ProductSearch.RequestFutures,
            ProductSearch.RequestLeverageds,
            ProductSearch.RequestLookup,
            ProductSearch.RequestOptions,
            ProductSearch.RequestStocks,
            ProductSearch.RequestWarrants,
        ],
        raw: bool = False,
    ) -> Union[ProductSearch, Dict, None]:
        connection_storage = self.connection_storage
        session_id = connection_storage.session_id
        session = self.session_storage.session
        credentials = self.credentials
        logger = self.logger

        return self.product_search(
            request=request,
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )
