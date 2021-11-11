# IMPORTATIONS STANDARD
import logging
import random
import time

# IMPORTATION THIRD PARTY
import pytest
import urllib3

# IMPORTATION INTERNAL
import degiro_connector.core.helpers.pb_handler as pb_handler
from degiro_connector.quotecast.models.quotecast_parser import QuotecastParser
from degiro_connector.quotecast.models.quotecast_pb2 import Chart, Quotecast

# SETUP LOGGING
logging.basicConfig(level=logging.FATAL)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# TESTS FEATURES
@pytest.mark.network
@pytest.mark.quotecast
def test_chart(quotecast_connected):
    time.sleep(random.uniform(0, 2))

    request = Chart.Request()
    request.requestid = "1"
    request.resolution = Chart.Interval.PT1M
    request.culture = "fr-FR"
    request.series.append("issueid:360148977")
    request.series.append("price:issueid:360148977")
    request.series.append("ohlc:issueid:360148977")
    request.series.append("volume:issueid:360148977")
    request.period = Chart.Interval.P1D
    request.tz = "Europe/Paris"

    # FETCH DATA
    chart = quotecast_connected.get_chart(
        request=request,
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
