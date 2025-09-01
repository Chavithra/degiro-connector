import logging


import requests
from orjson import loads

from degiro_connector.core.constants import urls
from degiro_connector.core.abstracts.abstract_action import AbstractAction
from degiro_connector.trading.models.credentials import Credentials
from degiro_connector.trading.models.product_search import (
    ProductBatch,
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

    @classmethod
    def product_search(
        cls,
        product_request: ProductRequest,
        session_id: str,
        credentials: Credentials,
        raw: bool = False,
        session: requests.Session | None = None,
        logger: logging.Logger | None = None,
    ) -> ProductBatch | dict | None:
        """Search products.
        Example 1:
            request = ProductBatch.LookupRequest(
                search_text='APPLE',
                limit=10,
                offset=0,
            )
        Example 2:
            request = ProductBatch.StocksRequest(
                index_id=5,
                is_in_us_green_list=False,
                stock_country_id=886,
                offset=0,
                limit=100,
                require_total=True,
                sort_columns='name',
                sort_types='asc',
            )
        Args:
            product_request (ProductRequest):
                Details of the products to search for.
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
            ProductBatch: API response.
        """

        if logger is None:
            logger = cls.build_logger()
        if session is None:
            session = cls.build_session()

        url = cls.URL_MATCHING[type(product_request)]

        params = product_request.model_dump(
            by_alias=True,
            exclude_none=True,
            mode="json",
        )

        if credentials.int_account is not None:
            params["intAccount"] = credentials.int_account

        params["sessionId"] = session_id

        http_request = requests.Request(method="GET", url=url, params=params)
        prepped = session.prepare_request(http_request)

        try:
            response = session.send(prepped)
            response.raise_for_status()

            if raw is True:
                product_search = loads(response.text)
            else:
                product_search = ProductBatch.model_validate_json(
                    json_data=response.text
                )

            return product_search
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
        product_request: ProductRequest,
        raw: bool = False,
    ) -> ProductBatch | dict | None:
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
