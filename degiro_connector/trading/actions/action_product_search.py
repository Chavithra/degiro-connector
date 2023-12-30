# IMPORTATION STANDARD
import logging
from typing import Dict, Union

# IMPORTATION THIRD PARTY
import requests
from google.protobuf import json_format

# IMPORTATION INTERNAL
from degiro_connector.core.constants import urls
from degiro_connector.core.abstracts.abstract_action import AbstractAction
from degiro_connector.trading.models.product_search import (
    ProductSearch,
    BondsRequest,
    ETFsRequest,
    FundsRequest,
    FuturesRequest,
    LeveragedsRequest,
    LookupRequest,
    OptionsRequest,
    StocksRequest,
    WarrantsRequest,
)
from degiro_connector.trading.models.trading_pb2 import Credentials

ProductRequest = (
    BondsRequest
    | ETFsRequest
    | FundsRequest
    | FuturesRequest
    | LeveragedsRequest
    | LookupRequest
    | OptionsRequest
    | StocksRequest
    | WarrantsRequest
)


class ActionProductSearch(AbstractAction):
    URL_MATCHING = {
        BondsRequest: urls.PRODUCT_SEARCH_BONDS,
        ETFsRequest: urls.PRODUCT_SEARCH_ETFS,
        FundsRequest: urls.PRODUCT_SEARCH_FUNDS,
        FuturesRequest: urls.PRODUCT_SEARCH_FUTURES,
        LeveragedsRequest: urls.PRODUCT_SEARCH_LEVERAGEDS,
        LookupRequest: urls.PRODUCT_SEARCH_LOOKUP,
        OptionsRequest: urls.PRODUCT_SEARCH_OPTIONS,
        StocksRequest: urls.PRODUCT_SEARCH_STOCKS,
        WarrantsRequest: urls.PRODUCT_SEARCH_WARRANTS,
    }

    # @staticmethod
    # def product_search_to_grpc(payload: dict) -> ProductSearch:
    #     product_search = ProductSearch()
    #     product_search.response_datetime.GetCurrentTime()
    #     json_format.ParseDict(
    #         js_dict=payload,
    #         message=product_search,
    #         ignore_unknown_fields=True,
    #         descriptor_pool=None,
    #     )

    #     return product_search

    @classmethod
    def product_search(
        cls,
        product_request: ProductRequest,
        session_id: str,
        credentials: Credentials,
        raw: bool = False,
        session: requests.Session | None = None,
        logger: logging.Logger | None = None,
    ) -> Union[ProductSearch, Dict, None]:
        """Search products.
        Args:
            request (StockList.Request):
                List of options that we want to retrieve from the endpoint.
                Example 1:
                    request = ProductSearch.LookupRequest(
                        search_text='APPLE',
                        limit=10,
                        offset=0,
                    )
                Example 2:
                    request = ProductSearch.StocksRequest(
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

        url = cls.URL_MATCHING[type(product_request)]

        params = product_request.model_dump(
            mode="json", by_alias=True, exclude_none=True
        )

        if credentials.int_account > 0:
            params["intAccount"] = credentials.int_account

        params["sessionId"] = session_id

        print(params)

        http_request = requests.Request(method="GET", url=url, params=params)
        prepped = session.prepare_request(http_request)
        response_raw = None

        try:
            response_raw = session.send(prepped)
            response_raw.raise_for_status()
            response_map = response_raw.json()

            if raw is True:
                product_search = response_map
            else:
                product_search = ProductSearch.model_validate(obj=response_map)

            return product_search
        except requests.HTTPError as e:
            logger.fatal(e)
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
        product_request: ProductRequest,
        raw: bool = False,
    ) -> Union[ProductSearch, Dict, None]:
        connection_storage = self.connection_storage
        session_id = connection_storage.session_id
        session = self.session_storage.session
        credentials = self.credentials
        logger = self.logger

        return self.product_search(
            product_request=product_request,
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )
