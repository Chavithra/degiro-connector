import logging
import degiro_connector.trading.utilities as utilities

from typing import Union
from degiro_connector.quotecast.constants.headers import Headers
from degiro_connector.trading.models.session_storage import (
    SessionStorage,
)
from degiro_connector.trading.pb.trading_pb2 import (
    AccountOverview,
    Agenda,
    CashAccountReport,
    CompanyProfile,
    CompanyRatios,
    Credentials,
    Favourites,
    FinancialStatements,
    LatestNews,
    NewsByCompany,
    Order,
    OrdersHistory,
    ProductsInfo,
    ProductSearch,
    TopNewsPreview,
    TransactionsHistory,
    Update,
)


class Basic:
    """ Tools to consume Degiro's Trading API.

    Same operations than "utilities" but with automatic management of :
        * credentials
        * requests.Session
        * logging.Logger
    """

    @property
    def credentials(self) -> Credentials:
        return self._credentials

    @property
    def session_storage(self) -> SessionStorage:
        return self._session_storage

    @session_storage.setter
    def session_storage(self, session_storage: SessionStorage):
        self._session_storage = session_storage

    def build_session_storage(self) -> SessionStorage:
        return SessionStorage(
            headers=Headers.get_headers(),
            hooks=None
        )

    def __init__(
        self,
        credentials: Credentials,
        session_storage: SessionStorage = None,
    ):
        if session_storage is None:
            session_storage = self.build_session_storage()

        self._logger = logging.getLogger(self.__module__)
        self._credentials = credentials
        self._session_storage = session_storage

    def get_session_id(self) -> str:
        credentials = self._credentials
        logger = self._logger
        session = self._session_storage.session

        return utilities.get_session_id(
            credentials=credentials,
            session=session,
            logger=logger
        )

    def logout(self, session_id: str) -> bool:
        credentials = self._credentials
        logger = self._logger
        session = self._session_storage.session

        return utilities.logout(
            session_id=session_id,
            credentials=credentials,
            session=session,
            logger=logger,
        )

    def get_update(
        self,
        request_list: Update.RequestList,
        session_id: str,
        raw: bool = False,
    ) -> Union[dict, Update]:
        credentials = self._credentials
        logger = self._logger
        session = self._session_storage.session

        return utilities.get_update(
            request_list=request_list,
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )

    def check_order(
        self,
        order: Order,
        session_id: str,
        raw: bool = False,
    ) -> Union[Order.CheckingResponse, bool]:
        credentials = self._credentials
        logger = self._logger
        session = self._session_storage.session

        return utilities.check_order(
            order=order,
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )

    def confirm_order(
        self,
        confirmation_id: str,
        order: Order,
        session_id: str,
        raw: bool = False,
    ) -> Union[Order.ConfirmationResponse, bool]:
        credentials = self._credentials
        logger = self._logger
        session = self._session_storage.session

        return utilities.confirm_order(
            confirmation_id=confirmation_id,
            order=order,
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )

    def update_order(
        self,
        order: Order,
        session_id: str,
    ) -> bool:
        credentials = self._credentials
        logger = self._logger
        session = self._session_storage.session

        return utilities.update_order(
            order=order,
            session_id=session_id,
            credentials=credentials,
            session=session,
            logger=logger,
        )

    def delete_order(
        self,
        order_id: str,
        session_id: str,
    ) -> bool:
        credentials = self._credentials
        logger = self._logger
        session = self._session_storage.session

        return utilities.delete_order(
            order_id=order_id,
            session_id=session_id,
            credentials=credentials,
            session=session,
            logger=logger,
        )

    def get_config(
        self,
        session_id: str,
    ) -> dict:
        logger = self._logger
        session = self._session_storage.session

        return utilities.get_config(
            session_id=session_id,
            session=session,
            logger=logger,
        )

    def get_client_details(
        self,
        session_id: str,
    ) -> dict:
        logger = self._logger
        session = self._session_storage.session

        return utilities.get_client_details(
            session_id=session_id,
            session=session,
            logger=logger,
        )

    def get_account_info(
        self,
        session_id: str,
    ) -> dict:
        credentials = self._credentials
        logger = self._logger
        session = self._session_storage.session

        return utilities.get_account_info(
            session_id=session_id,
            credentials=credentials,
            session=session,
            logger=logger,
        )

    def get_orders_history(
        self,
        request: OrdersHistory.Request,
        session_id: str,
        raw: bool = False,
    ) -> Union[dict, OrdersHistory]:
        credentials = self._credentials
        logger = self._logger
        session = self._session_storage.session

        return utilities.get_orders_history(
            request=request,
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )

    def get_transactions_history(
        self,
        request: TransactionsHistory.Request,
        session_id: str,
        raw: bool = False,
    ) -> Union[dict, TransactionsHistory]:
        credentials = self._credentials
        logger = self._logger
        session = self._session_storage.session

        return utilities.get_transactions_history(
            request=request,
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )

    def get_account_overview(
        self,
        request: AccountOverview.Request,
        session_id: str,
        raw: bool = False,
    ) -> Union[dict, AccountOverview]:
        credentials = self._credentials
        logger = self._logger
        session = self._session_storage.session

        return utilities.get_account_overview(
            request=request,
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )

    def product_search(
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
        session_id: str,
        raw: bool = False,
    ) -> Union[dict, ProductSearch]:
        credentials = self._credentials
        logger = self._logger
        session = self._session_storage.session

        return utilities.product_search(
            request=request,
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )

    def get_favourites_list(
        self,
        session_id: str,
        raw: bool = False,
    ) -> Union[dict, Favourites]:
        credentials = self._credentials
        logger = self._logger
        session = self._session_storage.session

        return utilities.get_favourites_list(
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )

    def get_products_config(
        self,
        session_id: str,
        raw: bool = False,
    ) -> Union[dict, ProductSearch.Config]:
        credentials = self._credentials
        logger = self._logger
        session = self._session_storage.session

        return utilities.get_products_config(
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )

    def get_products_info(
        self,
        request: ProductsInfo.Request,
        session_id: str,
        raw: bool = False,
    ) -> Union[dict, ProductsInfo]:
        credentials = self._credentials
        logger = self._logger
        session = self._session_storage.session

        return utilities.get_products_info(
            request=request,
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )

    def get_company_ratios(
        self,
        product_isin: str,
        session_id: str,
        raw: bool = False,
    ) -> Union[dict, CompanyRatios]:
        credentials = self._credentials
        logger = self._logger
        session = self._session_storage.session

        return utilities.get_company_ratios(
            product_isin=product_isin,
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )

    def get_company_profile(
        self,
        product_isin: str,
        session_id: str,
        raw: bool = False,
    ) -> Union[dict, CompanyProfile]:
        credentials = self._credentials
        logger = self._logger
        session = self._session_storage.session

        return utilities.get_company_profile(
            product_isin=product_isin,
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )

    def get_financial_statements(
        self,
        product_isin: str,
        session_id: str,
        raw: bool = False,
    ) -> Union[dict, FinancialStatements]:
        credentials = self._credentials
        logger = self._logger
        session = self._session_storage.session

        return utilities.get_financial_statements(
            product_isin=product_isin,
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )

    def get_latest_news(
        self,
        request: LatestNews.Request,
        session_id: str,
        raw: bool = False,
    ) -> Union[dict, LatestNews]:
        credentials = self._credentials
        logger = self._logger
        session = self._session_storage.session

        return utilities.get_latest_news(
            request=request,
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )

    def get_top_news_preview(
        self,
        session_id: str,
        raw: bool = False,
    ) -> Union[dict, TopNewsPreview]:
        credentials = self._credentials
        logger = self._logger
        session = self._session_storage.session

        return utilities.get_top_news_preview(
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )

    def get_news_by_company(
        self,
        request: NewsByCompany.Request,
        session_id: str,
        raw: bool = False,
    ) -> Union[dict, NewsByCompany]:
        credentials = self._credentials
        logger = self._logger
        session = self._session_storage.session

        return utilities.get_news_by_company(
            request=request,
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )

    def get_cash_account_report(
        self,
        request: CashAccountReport.Request,
        session_id: str,
        raw: bool = False,
    ) -> Union[dict, CashAccountReport]:
        credentials = self._credentials
        logger = self._logger
        session = self._session_storage.session

        return utilities.get_cash_account_report(
            request=request,
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )

    def get_agenda(
        self,
        request: Agenda.Request,
        session_id: str,
        raw: bool = False,
    ) -> Union[dict, Agenda]:
        credentials = self._credentials
        logger = self._logger
        session = self._session_storage.session

        return utilities.get_agenda(
            request=request,
            session_id=session_id,
            credentials=credentials,
            raw=raw,
            session=session,
            logger=logger,
        )


if __name__ == '__main__':
    # IMPORTATIONS
    import json

    from degiro_connector.trading.pb.trading_pb2 import Credentials

    # FETCH CONFIG
    with open('config.json') as config_file:
        config = json.load(config_file)

    # SETUP CREDENTIALS
    username = config['username']
    password = config['password']
    int_account = config['int_account']
    credentials = Credentials(
        int_account=int_account,
        username=username,
        password=password
    )
    # SETUP API
    basic = Basic(credentials=credentials)

    # ESTABLISH CONNECTION
    session_id = basic.get_session_id()
