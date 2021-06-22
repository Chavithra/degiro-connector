import logging

from degiro_connector.trading.basic import Basic
from degiro_connector.trading.models.connection_storage import (
    ConnectionStorage,
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
from typing import Union


class API:
    """ Tools to consume Degiro's QuoteCast API.

    Same operations than "Basic" but with "session_id" management.

    This class should be threadsafe.
    """

    @property
    def basic(self) -> Basic:
        return self._basic

    @property
    def connection_storage(self) -> ConnectionStorage:
        return self._connection_storage

    @property
    def credentials(self) -> int:
        return self._basic.credentials

    def __init__(self, credentials: Credentials):
        self._basic = Basic(credentials=credentials)

        self._connection_storage = ConnectionStorage(
            connection_timeout=1800,
        )
        self._connection_storage.setup_hooks(
            session=self._basic.session_storage.session,
        )
        self.logger = logging.getLogger(self.__module__)

    def connect(self) -> str:
        basic = self.basic
        connection_storage = self._connection_storage
        connection_storage.session_id = basic.get_session_id()

        return connection_storage.session_id

    def logout(self) -> bool:
        basic = self._basic
        session_id = self._connection_storage.session_id
        self._connection_storage.session_id = ''

        return basic.logout(session_id=session_id)

    def get_update(
        self,
        request_list: Update.RequestList,
        raw: bool = False,
    ) -> Union[dict, Update]:
        basic = self._basic
        session_id = self._connection_storage.session_id

        return basic.get_update(
            request_list=request_list,
            session_id=session_id,
            raw=raw,
        )

    def check_order(
        self,
        order: Order,
        raw: bool = False,
    ) -> Union[Order.ConfirmationResponse, bool]:
        basic = self._basic
        session_id = self._connection_storage.session_id

        return basic.check_order(
            order=order,
            session_id=session_id,
            raw=raw,
        )

    def confirm_order(
        self,
        confirmation_id: str,
        order: Order,
        raw: bool = False,
    ) -> Union[Order.ConfirmationResponse, bool]:
        basic = self._basic
        session_id = self._connection_storage.session_id

        return basic.confirm_order(
            confirmation_id=confirmation_id,
            order=order,
            session_id=session_id,
            raw=raw,
        )

    def update_order(self, order: Order) -> bool:
        basic = self._basic
        session_id = self._connection_storage.session_id

        return basic.update_order(
            order=order,
            session_id=session_id,
        )

    def delete_order(self, order_id: str) -> bool:
        basic = self._basic
        session_id = self._connection_storage.session_id

        return basic.delete_order(
            order_id=order_id,
            session_id=session_id
        )

    def get_config(self) -> dict:
        basic = self._basic
        session_id = self._connection_storage.session_id

        return basic.get_config(
            session_id=session_id,
        )

    def get_client_details(self) -> dict:
        basic = self._basic
        session_id = self._connection_storage.session_id

        return basic.get_client_details(
            session_id=session_id,
        )

    def get_account_info(self) -> dict:
        basic = self._basic
        session_id = self._connection_storage.session_id

        return basic.get_account_info(
            session_id=session_id,
        )

    def get_orders_history(
        self,
        request: OrdersHistory.Request,
        raw: bool = False,
    ) -> Union[dict, Update]:
        basic = self._basic
        session_id = self._connection_storage.session_id

        return basic.get_orders_history(
            request=request,
            session_id=session_id,
            raw=raw,
        )

    def get_transactions_history(
        self,
        request: TransactionsHistory.Request,
        raw: bool = False,
    ) -> Union[dict, Update]:
        basic = self._basic
        session_id = self._connection_storage.session_id

        return basic.get_transactions_history(
            request=request,
            session_id=session_id,
            raw=raw,
        )

    def get_account_overview(
        self,
        request: AccountOverview.Request,
        raw: bool = False,
    ) -> Union[dict, AccountOverview]:
        basic = self._basic
        session_id = self._connection_storage.session_id

        return basic.get_account_overview(
            request=request,
            session_id=session_id,
            raw=raw,
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
        raw: bool = False,
    ) -> Union[dict, ProductSearch]:
        basic = self._basic
        session_id = self._connection_storage.session_id

        return basic.product_search(
            request=request,
            session_id=session_id,
            raw=raw,
        )

    def get_favourites_list(
        self,
        raw: bool = False,
    ) -> Union[dict, Favourites]:
        basic = self._basic
        session_id = self._connection_storage.session_id

        return basic.get_favourites_list(
            session_id=session_id,
            raw=raw,
        )

    def get_products_config(
        self,
        raw: bool = False,
    ) -> Union[dict, ProductSearch.Config]:
        basic = self._basic
        session_id = self._connection_storage.session_id

        return basic.get_products_config(
            session_id=session_id,
            raw=raw,
        )

    def get_products_info(
        self,
        request: ProductsInfo.Request,
        raw: bool = False,
    ) -> Union[dict, ProductsInfo]:
        basic = self._basic
        session_id = self._connection_storage.session_id

        return basic.get_products_info(
            request=request,
            session_id=session_id,
            raw=raw,
        )

    def get_company_ratios(
        self,
        product_isin: str,
        raw: bool = False,
    ) -> Union[dict, CompanyRatios]:
        basic = self._basic
        session_id = self._connection_storage.session_id

        return basic.get_company_ratios(
            product_isin=product_isin,
            session_id=session_id,
            raw=raw,
        )

    def get_company_profile(
        self,
        product_isin: str,
        raw: bool = False,
    ) -> Union[dict, CompanyProfile]:
        basic = self._basic
        session_id = self._connection_storage.session_id

        return basic.get_company_profile(
            product_isin=product_isin,
            session_id=session_id,
            raw=raw,
        )

    def get_financial_statements(
        self,
        product_isin: str,
        raw: bool = False,
    ) -> Union[dict, FinancialStatements]:
        basic = self._basic
        session_id = self._connection_storage.session_id

        return basic.get_financial_statements(
            product_isin=product_isin,
            session_id=session_id,
            raw=raw,
        )

    def get_latest_news(
        self,
        request: LatestNews.Request,
        raw: bool = False,
    ) -> Union[dict, LatestNews]:
        basic = self._basic
        session_id = self._connection_storage.session_id

        return basic.get_latest_news(
            request=request,
            session_id=session_id,
            raw=raw,
        )

    def get_top_news_preview(
        self,
        raw: bool = False,
    ) -> Union[dict, TopNewsPreview]:
        basic = self._basic
        session_id = self._connection_storage.session_id

        return basic.get_top_news_preview(
            session_id=session_id,
            raw=raw,
        )

    def get_news_by_company(
        self,
        request: NewsByCompany.Request,
        raw: bool = False,
    ) -> Union[dict, NewsByCompany]:
        basic = self._basic
        session_id = self._connection_storage.session_id

        return basic.get_news_by_company(
            request=request,
            session_id=session_id,
            raw=raw,
        )

    def get_cash_account_report(
        self,
        request: CashAccountReport.Request,
        raw: bool = False,
    ) -> Union[dict, CashAccountReport]:
        basic = self._basic
        session_id = self._connection_storage.session_id

        return basic.get_cash_account_report(
            request=request,
            session_id=session_id,
            raw=raw,
        )

    def get_agenda(
        self,
        request: Agenda.Request,
        raw: bool = False,
    ) -> Union[dict, Agenda]:
        basic = self._basic
        session_id = self._connection_storage.session_id

        return basic.get_agenda(
            request=request,
            session_id=session_id,
            raw=raw,
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
    api = API(credentials=credentials)

    # ESTABLISH CONNECTION
    api.connect()
    session_id = api.connection_storage.session_id
