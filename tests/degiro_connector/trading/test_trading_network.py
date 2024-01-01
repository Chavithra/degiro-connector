# IMPORTATIONS STANDARD
import datetime
import logging
import random
import time

import pytest
import urllib3

from degiro_connector.trading.models.trading_pb2 import (
    AccountOverview,
    Agenda,
    CashAccountReport,
    CompanyProfile,
    CompanyRatios,
    Favourites,
    FinancialStatements,
    LatestNews,
    NewsByCompany,
    OrdersHistory,
    ProductSearch,
    ProductsInfo,
    TopNewsPreview,
    TransactionsHistory,
    Update,
)

logging.basicConfig(level=logging.FATAL)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# TESTS FEATURES
@pytest.mark.network
@pytest.mark.trading
def test_config_table(user_token, trading_connected):
    time.sleep(random.uniform(0, 2))

    real_user_token = user_token
    real_session_id = trading_connected.connection_storage.session_id
    config_table = trading_connected.get_config()
    user_token = config_table["clientId"]
    session_id = config_table["sessionId"]

    assert user_token == real_user_token
    assert session_id == real_session_id


@pytest.mark.network
@pytest.mark.trading
def test_config_table_urls(trading_connected):
    time.sleep(random.uniform(0, 2))

    config_table = trading_connected.get_config()

    assert config_table["paUrl"] == "https://trader.degiro.nl/pa/secure/"
    assert (
        config_table["productSearchUrl"]
        == "https://trader.degiro.nl/product_search/secure/"
    )
    assert (
        config_table["companiesServiceUrl"]
        == "https://trader.degiro.nl/dgtbxdsservice/"
    )
    assert config_table["reportingUrl"] == "https://trader.degiro.nl/reporting/secure/"
    assert config_table["tradingUrl"] == "https://trader.degiro.nl/trading/secure/"


@pytest.mark.network
@pytest.mark.trading
def test_get_account_info(trading_connected):
    time.sleep(random.uniform(0, 2))

    # FETCH DATA
    account_info_table = trading_connected.get_account_info()

    data_keys = [
        "clientId",
        "baseCurrency",
        "currencyPairs",
        "marginType",
        "cashFunds",
        "compensationCapping",
    ]

    assert isinstance(account_info_table, dict)
    for key in data_keys:
        assert key in account_info_table["data"]


@pytest.mark.network
@pytest.mark.trading
def test_get_account_overview(trading_connected):
    time.sleep(random.uniform(0, 2))

    # SETUP REQUEST
    today = datetime.date.today()
    from_date = AccountOverview.Request.Date(
        year=2020,
        month=1,
        day=1,
    )
    to_date = AccountOverview.Request.Date(
        year=today.year,
        month=today.month,
        day=today.day,
    )
    request = AccountOverview.Request(
        from_date=from_date,
        to_date=to_date,
    )

    # FETCH DATA
    account_overview = trading_connected.get_account_overview(
        request=request,
        raw=False,
    )

    assert isinstance(account_overview, AccountOverview)


@pytest.mark.network
@pytest.mark.trading
def test_get_agenda(trading_connected):
    time.sleep(random.uniform(0, 2))

    # SETUP REQUEST
    request = Agenda.Request()
    request.start_date.FromJsonString("2021-06-21T22:00:00Z")
    request.end_date.FromJsonString("2021-11-28T23:00:00Z")
    request.calendar_type = Agenda.CalendarType.DIVIDEND_CALENDAR
    request.offset = 0
    request.limit = 25  # 0 < limit <= 100

    # FETCH DATA
    agenda = trading_connected.get_agenda(
        request=request,
        raw=False,
    )

    assert isinstance(agenda, Agenda)


@pytest.mark.network
@pytest.mark.trading
def test_get_cash_account_report(trading_connected):
    time.sleep(random.uniform(0, 2))

    # SETUP REQUEST
    today = datetime.date.today()
    from_date = CashAccountReport.Request.Date(
        year=today.year,
        month=1,
        day=1,
    )
    to_date = CashAccountReport.Request.Date(
        year=today.year,
        month=today.month,
        day=today.day,
    )
    request = CashAccountReport.Request(
        format=CashAccountReport.Format.CSV,
        country="FR",
        lang="fr",
        from_date=from_date,
        to_date=to_date,
    )

    # FETCH DATA
    cash_account_report = trading_connected.get_cash_account_report(
        request=request,
        raw=False,
    )
    format = cash_account_report.Format.Name(cash_account_report.format)
    content = cash_account_report.content

    assert isinstance(cash_account_report, CashAccountReport)
    assert format == "CSV"
    assert isinstance(content, str)


@pytest.mark.network
@pytest.mark.trading
def test_get_client_details(trading_connected):
    time.sleep(random.uniform(0, 2))

    # FETCH DATA
    client_details_table = trading_connected.get_client_details()

    data_keys = [
        "id",
        "intAccount",
        "loggedInPersonId",
        "clientRole",
        "effectiveClientRole",
        "contractType",
        "username",
        "displayName",
        "email",
        "firstContact",
        "address",
        "cellphoneNumber",
        "locale",
        "language",
        "culture",
        "displayLanguage",
        "bankAccount",
        "flatexBankAccount",
        "memberCode",
        "isWithdrawalAvailable",
        "isAllocationAvailable",
        "isIskClient",
        "isCollectivePortfolio",
        "isAmClientActive",
        "canUpgrade",
    ]

    assert isinstance(client_details_table, dict)
    for key in data_keys:
        assert key in client_details_table["data"]


@pytest.mark.network
@pytest.mark.trading
def test_get_company_profile(trading_connected):
    time.sleep(random.uniform(0, 2))

    # FETCH DATA
    product_isin = "FR0000131906"
    company_profile = trading_connected.get_company_profile(
        product_isin=product_isin,
        raw=False,
    )

    assert isinstance(company_profile, CompanyProfile)


@pytest.mark.network
@pytest.mark.trading
def test_get_company_ratios(trading_connected):
    time.sleep(random.uniform(0, 2))

    # FETCH DATA
    product_isin = "FR0000131906"
    company_ratios = trading_connected.get_company_ratios(
        product_isin=product_isin,
        raw=False,
    )

    assert isinstance(company_ratios, CompanyRatios)


@pytest.mark.network
@pytest.mark.trading
def test_get_favourites_list(trading_connected):
    time.sleep(random.uniform(0, 2))

    # FETCH DATA
    favourites_list = trading_connected.get_favourites_list(raw=False)

    assert isinstance(favourites_list, Favourites)


@pytest.mark.network
@pytest.mark.trading
def test_get_financial_statements(trading_connected):
    time.sleep(random.uniform(0, 2))

    # FETCH DATA
    product_isin = "FR0000131906"
    financial_statements = trading_connected.get_financial_statements(
        product_isin=product_isin,
        raw=False,
    )

    assert isinstance(financial_statements, FinancialStatements)


@pytest.mark.network
@pytest.mark.trading
def test_get_latest_news(trading_connected):
    time.sleep(random.uniform(0, 2))

    # SETUP REQUEST
    request = LatestNews.Request(
        offset=0,
        languages="en,fr",
        limit=20,
    )

    # FETCH DATA
    latest_news = trading_connected.get_latest_news(request=request, raw=False)

    assert isinstance(latest_news, LatestNews)


@pytest.mark.network
@pytest.mark.trading
def test_get_news_by_company(trading_connected):
    time.sleep(random.uniform(0, 2))

    # SETUP REQUEST
    request = NewsByCompany.Request(
        isin="NL0000235190",
        limit=10,
        offset=0,
        languages="en,fr",
    )

    # FETCH DATA
    news_by_company = trading_connected.get_news_by_company(request=request, raw=False)

    assert isinstance(news_by_company, NewsByCompany)


@pytest.mark.network
@pytest.mark.trading
def test_get_orders_history(trading_connected):
    time.sleep(random.uniform(0, 2))

    # SETUP REQUEST
    today = datetime.date.today()
    from_date = OrdersHistory.Request.Date(
        year=today.year,
        month=10,
        day=1,
    )
    to_date = OrdersHistory.Request.Date(
        year=today.year,
        month=today.month,
        day=today.day,
    )
    request = OrdersHistory.Request(
        from_date=from_date,
        to_date=to_date,
    )

    # FETCH DATA
    orders_history = trading_connected.get_orders_history(
        request=request,
        raw=False,
    )

    assert isinstance(orders_history, OrdersHistory)


@pytest.mark.network
@pytest.mark.trading
def test_product_search(trading_connected):
    time.sleep(random.uniform(0, 2))

    # SETUP REQUEST
    request_lookup = ProductSearch.RequestLookup(
        search_text="APPLE",
        limit=2,
        offset=0,
        product_type_id=1,
    )

    # FETCH DATA
    products_lookup = trading_connected.product_search(
        request=request_lookup,
        raw=False,
    )

    assert isinstance(products_lookup, ProductSearch)


@pytest.mark.network
@pytest.mark.trading
def test_get_products_config(trading_connected):
    time.sleep(random.uniform(0, 2))

    # FETCH DATA
    products_config = trading_connected.get_products_config(raw=False)

    assert isinstance(products_config, ProductSearch.Config)


@pytest.mark.network
@pytest.mark.trading
def test_get_products_info(trading_connected):
    time.sleep(random.uniform(0, 2))

    # SETUP REQUEST
    request = ProductsInfo.Request()
    request.products.extend([96008, 1153605, 5462588])

    # FETCH DATA
    products_info = trading_connected.get_products_info(
        request=request,
        raw=False,
    )

    assert isinstance(products_info, ProductsInfo)


@pytest.mark.network
@pytest.mark.trading
def test_get_top_news_preview(trading_connected):
    time.sleep(random.uniform(0, 2))

    # FETCH DATA
    top_news_preview = trading_connected.get_top_news_preview(raw=False)

    assert isinstance(top_news_preview, TopNewsPreview)


@pytest.mark.network
@pytest.mark.trading
def test_get_transactions_history(trading_connected):
    time.sleep(random.uniform(0, 2))

    # SETUP REQUEST
    today = datetime.date.today()
    from_date = TransactionsHistory.Request.Date(
        year=today.year,
        month=today.month,
        day=1,
    )
    to_date = TransactionsHistory.Request.Date(
        year=today.year,
        month=today.month,
        day=today.day,
    )
    request = TransactionsHistory.Request(
        from_date=from_date,
        to_date=to_date,
    )

    # FETCH DATA
    transactions_history = trading_connected.get_transactions_history(
        request=request,
        raw=False,
    )

    assert isinstance(transactions_history, TransactionsHistory)


@pytest.mark.network
@pytest.mark.trading
def test_get_update(trading_connected):
    time.sleep(random.uniform(0, 2))

    # SETUP REQUEST
    request_list = Update.RequestList()
    request_list.values.extend(
        [
            Update.Request(option=Update.Option.ORDERS, last_updated=0),
            Update.Request(option=Update.Option.PORTFOLIO, last_updated=0),
            Update.Request(option=Update.Option.TOTALPORTFOLIO, last_updated=0),
        ]
    )

    # FETCH DATA
    update = trading_connected.get_update(request_list=request_list, raw=False)

    assert isinstance(update, Update)
