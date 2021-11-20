# IMPORTATIONS STANDARD
import logging
import random
import time

# IMPORTATION THIRD PARTY
import pandas
import pytest
import urllib3

# IMPORTATION INTERNAL
import degiro_connector.core.helpers.pb_handler as pb_handler
from degiro_connector.quotecast.actions.action_get_chart import ChartHelper
from degiro_connector.quotecast.models.quotecast_parser import QuotecastParser
from degiro_connector.quotecast.models.quotecast_pb2 import Quotecast

# SETUP LOGGING
logging.basicConfig(level=logging.FATAL)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# TESTS FEATURES
@pytest.mark.network
@pytest.mark.quotecast
def test_chart(quotecast_connected, stock_request):
    time.sleep(random.uniform(0, 2))

    # FETCH DATA
    chart = quotecast_connected.get_chart(
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
    chart0_df = ChartHelper.serie_to_df(serie=chart.series[1])

    assert isinstance(chart0_df, pandas.DataFrame)
    assert len(chart0_df) > 0


@pytest.mark.quotecast
@pytest.mark.network
def test_quotecast(quotecast_connected):
    time.sleep(random.uniform(0, 2))

    request = Quotecast.Request()
    request.subscriptions["AAPL.BATS,E"].extend(
        [
            "LastDate",
            "LastTime",
            "LastPrice",
            "LastVolume",
            "AskPrice",
            "BidPrice",
        ]
    )
    quotecast_connected.subscribe(request=request)

    quotecast = quotecast_connected.fetch_data()

    quotecast_parser = QuotecastParser()
    quotecast_parser.put_quotecast(quotecast=quotecast)
    ticker = quotecast_parser.ticker
    ticker_dict = pb_handler.message_to_dict(message=ticker)
    metrics = ticker_dict["products"]["AAPL.BATS,E"]["metrics"]

    assert "AAPL.BATS,E" in ticker.product_list

    for metric in metrics:
        assert isinstance(metrics[metric], float)
