import logging
import random
import time

import pandas
import pytest
import urllib3

from degiro_connector.core.models.model_connection import ModelConnection
from degiro_connector.quotecast.tools.chart_fetcher import ChartFetcher
from degiro_connector.quotecast.models.ticker import TickerRequest
from degiro_connector.quotecast.tools.ticker_fetcher import TickerFetcher
from degiro_connector.quotecast.tools.ticker_to_df import TickerToDF


# SETUP LOGGING
logging.basicConfig(level=logging.FATAL)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# TESTS FEATURES
@pytest.mark.network
@pytest.mark.quotecast
def test_chart(stock_request, user_token):
    time.sleep(random.uniform(0, 2))

    chart_fetcher = ChartFetcher(
        user_token=user_token,
        connection_storage=ModelConnection(timeout=600)
    )

    # FETCH DATA
    chart = chart_fetcher.get_chart(
        request=stock_request,
        raw=True,
    )

    b_series_0_data_keys = [
        "issueId",
        "companyId",
        "name",
        "identifier",
        "isin",
        "alfa",
        "market",
        "currency",
        "type",
        "quality",
        "lastPrice",
        "lastTime",
        "absDiff",
        "relDiff",
        "highPrice",
        "highTime",
        "lowPrice",
        "lowTime",
        "openPrice",
        "openTime",
        "closePrice",
        "closeTime",
        "cumulativeVolume",
        "previousClosePrice",
        "previousCloseTime",
        "tradingStartTime",
        "tradingEndTime",
        "tradingAddedTime",
        "lowPriceP1Y",
        "highPriceP1Y",
        "windowStart",
        "windowEnd",
        "windowFirst",
        "windowLast",
        "windowHighTime",
        "windowHighPrice",
        "windowLowTime",
        "windowLowPrice",
        "windowOpenTime",
        "windowOpenPrice",
        "windowPreviousCloseTime",
        "windowPreviousClosePrice",
        "windowTrend",
    ]

    series_0_data_keys = list(chart["series"][0]["data"].keys())

    assert b_series_0_data_keys == series_0_data_keys
    assert chart["requestid"] == "1"
    assert chart["resolution"] == "PT1M"
    assert chart["series"][0]["data"]["quality"] == "REALTIME"
    assert chart["series"][0]["data"]["issueId"] == 360148977


@pytest.mark.quotecast
@pytest.mark.network
def test_format_chart(quotecast_connected, stock_request):
    time.sleep(random.uniform(0, 2))

    # FETCH DATA
    chart = quotecast_connected.get_chart(
        request=stock_request,
        raw=False,
    )

    ChartHelper.format_chart(chart=chart, copy=False)
    chart1 = chart.series[1]
    chart1_df = ChartHelper.serie_to_df(serie=chart1)

    assert isinstance(chart1_df, pandas.DataFrame)
    assert len(chart1_df) == len(chart1.data)

    for index, row in chart1_df.iterrows():
        assert row.price == chart1.data[index][1]


@pytest.mark.quotecast
@pytest.mark.network
def test_quotecast(user_token):
    time.sleep(random.uniform(0, 2))

    ticker_to_df = TickerToDF()
    product_list = [
        "AAPL.BATS,E",  # Apple 
        "360017018",    # Air Liquide
        "360114899",    # AIRBUS
        "365019496",    # Alstom
    ]
    ticker_request = TickerRequest(
        request_type="subscription",
        request_map={
            "360015751": [
                "LastDate",
                "LastTime",
                "LastPrice",
                "LastVolume",
            ],
            "AAPL.BATS,E": [
                'LastDate',
                'LastTime',
                'LastPrice',
                'LastVolume',
            ],
        },
    )

    session_id = TickerFetcher.get_session_id(user_token=user_token)

    if session_id is None:
        raise TypeError("`session_id` is None")

    TickerFetcher.subscribe(
        ticker_request=ticker_request,
        session_id=session_id,
    )

    ticker = TickerFetcher.fetch_ticker(session_id=session_id)


    if ticker is None:
        raise TypeError("`ticker` is None")

    df = ticker_to_df.parse(ticker=ticker)

    assert isinstance(df, pl.DataFrame)
