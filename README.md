# 1. **Degiro Connector**

This is yet another library to access Degiro's API.

## 1.1. Contribution

⭐️ Hopefully you have starred the project ⭐️

You can contribute to the project in two ways :

**Code and documentation** : pull requests are welcome !

**Feedback** : feel free to open an issue or send me a message if you have a feedback or question.

## 1.2. Installation

```bash
# INSTALL
pip install degiro-connector

# UPGRADE
pip install --no-cache-dir --upgrade degiro-connector

# UNINSTALL
pip uninstall degiro-connector
```

## 1.3. Features
Here are the features you can access through this library :

|**Endpoint**|**Feature(s)**|
|:-|:-|
|AccountCashReport|Export cash movements in a specific format : CSV, HTML, PDF or XLS.|
|AccountInfo|Retrieve a table containing : "clientId" and Currencies.|
|AccountOverview|Retrieve all the cash movements between two dates.|
|Agenda|Crucial events regarding products : Dividend, Economic, Earnings, Holiday, IPO or Split.|
|Bonds<br>ETFs<br>Funds<br>Futures<br>Leverageds<br>Lookup<br>Options<br>Stocks<br>Warrants|Search list of products according their name, type and other criterias. <br> For instance all the stocks from NASDAQ 100.|
|Chart|Retrieve chart data.|
|ClientDetails|Retrieve a table containing : "clientId", "intAccount" and other account information.|
|CompanyProfile|Retrieve a company's profile using its ISIN code.|
|CompanyRatios|Retrieve a company's ratios using its ISIN code.|
|Config|Retrieve a table containing : "clientId" and URLs which are constitutive of Degiro's API.|
|EstimatesSummaries|Retrieve a company's estimates summaries using its ISIN code.|
|Favorites|Add/Delete/Prioritize/Retrieve favorites lists.|
|FavoritesProducts|Add/Update products associated with a favorite list.|
|FinancialStatements|Retrieve a company's financial statements using its ISIN code.|
|LatestNews|Retrieve latest news about all the companies.|
|LoginQuotecast|Establish a connection for quotecast operations.|
|LoginTrading|Establish a connection for trading operations.|
|LogoutTrading|Destroy previously established connection for trading operations.|
|NewsByCompany|Retrieve news related to a specific company.|
|Order|Create, update, delete an Order.|
|OrderHistory|Retrieve all Orders created between two dates.|
|Orders|List pending Orders.|
|Portfolio|List products in your Portfolio.|
|ProductsConfig|Retrieve a table containing : useful parameters to filter products.|
|ProductsInfo|Search for products using their ids.|
|Quotecasts|Fetch real-time data on financial products. <br> For instance the real-time stock Price.|
|TopNewsPreview|Retrieve some news preview about all the companies.|
|TotalPorfolio|Retrieve aggregated information about your assets.|
|TransactionsHistory|Retrieve all Transactions created between two dates.|
|Underlyings|List Underlyings for Futures and Options.|

## 1.4. Table of contents
- [1. **Degiro Connector**](#1-degiro-connector)
  * [1.1. Contribution](#11-contribution)
  * [1.2. Installation](#13-installation)
  * [1.3. Features](#12-Features)
  * [1.4. Table of contents](#16-table-of-contents)
- [2. Real-time data](#2-real-time-data)
  * [2.1. What are the workflows ?](#21-what-are-the-workflows-)
  * [2.2. How to find your `user_token` ?](#22-how-to-find-your-user_token-)
  * [2.3. How to get a Chart ?](#23-how-to-get-a-chart-)
  * [2.4. How to format a chart.series ?](#24-how-to-format-a-chartseries-)
  * [2.5. How to find a product `vwd_id` ?](#25-how-to-find-a-product-vwd_id-)
  * [2.6. What are the credentials ?](#26-what-are-the-credentials-)
  * [2.7. How to connect ?](#27-how-to-connect-)
  * [2.8. Is there a timeout ?](#28-is-there-a-timeout-)
  * [2.9. How to subscribe to a data-stream ?](#29-how-to-subscribe-to-a-data-stream-)
  * [2.10. How to unsubscribe to a data-stream ?](#210-how-to-unsubscribe-to-a-data-stream-)
  * [2.11. How to fetch the data ?](#211-how-to-fetch-the-data-)
  * [2.12. How to use this data ?](#212-how-to-use-this-data-)
  * [2.13. Which are the available data types ?](#213-which-are-the-available-data-types-)
  * [2.14. What is a Ticker ?](#214-what-is-a-ticker-)
  * [2.15. What is inside the list[Metric] ?](#215-what-is-inside-the-listmetric-)
  * [2.16. What is inside the DataFrame ?](#216-what-is-inside-the-dataframe-)
- [3. Trading connection](#3-trading-connection)
  * [3.1. How to login ?](#31-how-to-login-)
  * [3.2. How to logout ?](#32-how-to-logout-)
  * [3.3. What are the credentials ?](#33-what-are-the-credentials-)
  * [3.4. How to find your : int_account ?](#34-how-to-find-your--int_account-)
  * [3.5. How to use 2FA ?](#35-how-to-use-2fa-)
  * [3.6. How to find your : totp_secret_key ?](#36-how-to-find-your--totp_secret_key-)
  * [3.7. How to find your : one_time_password ?](#37-how-to-find-your--one_time_password-)
  * [3.8. Is there a timeout ?](#38-is-there-a-timeout-)
  * [3.9. How to manage : TimeoutError ?](#39-how-to-manage--TimeoutError-)
- [4. Order](#4-order)
  * [4.1. How to create an Order ?](#41-how-to-create-an-order-)
  * [4.1.1. Check Order](#411-check-order)
  * [4.1.2. Confirm Order](#412-confirm-order)
  * [4.2. How to update an Order ?](#42-how-to-update-an-order-)
  * [4.3. How to delete an Order ?](#43-how-to-delete-an-order-)
- [5. Portfolio](#5-portfolio)
  * [5.1. How to retrieve pending Orders ?](#51-how-to-retrieve-pending-orders-)
  * [5.2. How to get the Portfolio ?](#52-how-to-get-the-portfolio-)
  * [5.3. How to get the TotalPortfolio ?](#53-how-to-get-the-totalportfolio-)
  * [5.4. How to retrieve the OrdersHistory ?](#54-how-to-retrieve-the-ordershistory-)
  * [5.5. How to retrieve the TransactionsHistory ?](#55-how-to-retrieve-the-transactionshistory-)
  * [5.6. How to retrieve Upcoming Payments ?](#55-how-to-retrieve-the-upcoming-payments-)
- [6. Account](#6-account)
  * [6.1. How to retrieve the table : Config ?](#61-how-to-retrieve-the-table--config-)
  * [6.2. How to retrieve the table : ClientDetails ?](#62-how-to-retrieve-the-table--clientdetails-)
  * [6.3. How to retrieve the table : AccountInfo ?](#63-how-to-retrieve-the-table--accountinfo-)
  * [6.4. How to get the table : AccountOverview ?](#64-how-to-get-the-table--accountoverview-)
  * [6.5. How to export the table : AccountReport ?](#65-how-to-export-the-table--accountreport-)
  * [6.6. How to export the table : PositionReport ?](#66-how-to-export-the-table--positionreport-)
- [7. Products](#7-products)
  * [7.1. How to get the table : ProductsConfig ?](#71-how-to-get-the-table--productsconfig-)
  * [7.2. How to lookup products (search by name) ?](#72-how-to-lookup-products-search-by-name-)
  * [7.3. How to search bonds ?](#73-how-to-search-bonds-)
  * [7.4. How to search etfs ?](#74-how-to-search-etfs-)
  * [7.5. How to search funds ?](#75-how-to-search-funds-)
  * [7.6. How to search futures ?](#76-how-to-search-futures-)
  * [7.7. How to search leverageds ?](#77-how-to-search-leverageds-)
  * [7.8. How to search options ?](#78-how-to-search-options-)
  * [7.9. How to search stocks ?](#79-how-to-search-stocks-)
  * [7.10. How to search warrants ?](#710-how-to-search-warrants-)
  * [7.11. How to search products from ids ?](#711-how-to-search-products-from-ids-)
  * [7.12. How to get my favorite products ?](#712-how-to-get-my-favorite-products-)
  * [7.13. How to create a favorite list ?](#713-how-to-create-a-favorite-list-)
  * [7.14. How to delete a favorite list ?](#714-how-to-delete-a-favorite-list-)
  * [7.15. How to move a favorite list ?](#715-how-to-move-a-favorite-list-)
  * [7.16. How to put favorite list products ?](#716-how-to-put-favorite-list-products-)
  * [7.17. How to delete favorite list products ?](#717-how-to-delete-favorite-list-products-)
  * [7.18. How to get futures/options underlyings ?](#718-how-to-get-futuresoptions-underlyings-)
- [8. Companies](#8-companies)
  * [8.1. How to get : CompanyProfile ?](#81-how-to-get--companyprofile-)
  * [8.2. How to get : CompanyRatios ?](#82-how-to-get--companyratios-)
  * [8.3. How to get : FinancialStatements ?](#83-how-to-get--financialstatements-)
  * [8.4. How to get : LatestNews ?](#84-how-to-get--latestnews-)
  * [8.5. How to get : TopNewsPreview ?](#85-how-to-get--topnewspreview-)
  * [8.6. How to get : NewsByCompany ?](#86-how-to-get--newsbycompany-)
  * [8.7. How to get : Agenda ?](#87-how-to-get--agenda-)
  * [8.8. How to get : EstimatesSummaries ?](#88-how-to-get--estimatessummaries-)
- [9. License](#9-license)

# 2. Real-time data

It is possible to fetch the following data from Degiro's API:
- Charts series data
- Streams of data in real-time

## 2.1. What are the workflows ?

**CHARTS**

To consume charts series :

    A. Fetch charts : directly with your "user_token".
    B. Convert to a DataFrame.

**REAL-TIME**

To consume real-time data-stream :

    A. Connect : with your "user_token".
    B. Subscribe to metrics.
    C. Fetch these metrics.
    D. Convert to a DataFrame.


All the details of these steps are explained in the rest of this section.

## 2.2. How to find your `user_token` ?
You can find your "user_token" inside one of these tables :
* "Config" : attribute "clientId"
* "ClientDetails" : attribute "id"

See sections related to ["Config"](#61-how-to-retrieve-the-table--config-) and ["ClientDetails"](#62-how-to-retrieve-the-table--clientdetails-) tables.


## 2.3. How to get a Chart ?
You can fetch an object containing the same data than in Degiro's website graph.

For that you need to prepare a ChartRequest.

Here is a table with the available attributes for ChartRequest.

|**Parameter**|**Type**|**Description**|
|:-|:-|:-|
|requestid|str|It sends you back whatever string you put here, you can set it to : "1".|
|resolution|Chart.Resolution|Resolution of the chart like : Chart.Resolution.PT1M.|
|culture|str|Country code like : "en-US" or "fr-FR".|
|period|Chart.Period|Period of the chart, like : Chart.Period.P1D.|
|series|repeated string|Data to get like : ['issueid:36014897', 'price:issueid:360148977'].|
|tz|str|Timezone like : "Europe/Paris"|

Example of code :

```python
chart_fetcher = ChartFetcher(user_token=user_token)
chart_request = ChartRequest(
    culture="fr-FR",
    # override={
    #     "resolution": "P1D",
    #     "period": "P1W",
    # },
    period=Interval.P1D,
    requestid="1",
    resolution=Interval.PT60M,
    series=[
        "issueid:360148977",
        "price:issueid:360148977",
        "ohlc:issueid:360148977",
        "volume:issueid:360148977",
        # "vwdkey:AAPL.BATS,E",
        # "price:vwdkey:AAPL.BATS,E",
        # "ohlc:vwdkey:AAPL.BATS,E",
        # "volume:vwdkey:AAPL.BATS,E",
    ],
    tz="Europe/Paris",
)
chart = chart_fetcher.get_chart(
    chart_request=chart_request,
    raw=False,
)
```

The `issueid` parameter is the `vwd_id` of the product from which you want the `Chart` data.

See the section related to `vwd_id` for more information.

All the models are described in this module :
[chart.py](degiro_connector/quotecast/models/chart.py)

For a more comprehensive example :
 - [chart.py](examples/quotecast/chart.py)

## 2.4. How to format a chart.series ?

A Chart object contains a list of series.

There is a SeriesFormatter to help you convertir a series into a `polars.DataFrame`.

```python
df = SeriesFormatter.format(series=chart.series)
print(df)
```

Here are the result for different series.id.

- `issueid:360148977`

| issueId   | companyId | name      | identifier | ... | windowPreviousClosePrice | windowEndPrice |
|-----------|-----------|-----------|------------|-----|---------------------------|----------------|
| i64       | i64       | str       | str        | ... | f64                       | f64            |
| 360148977 | 9245      | Crédit    | issueid:3  | ... | 12.858                    | -0.00047       |

- `price:issueid:360148977`

| timestamp                  | price  |
|----------------------------|--------|
| datetime[μs]               | f64    |
| 2023-12-29 09:00:00        | 12.858 |
| 2023-12-29 10:58:58.800    | 12.85  |
| ...                        | ...    |
| 2023-12-29 17:28:58.800    | 12.83  |
| 2023-12-29 17:34:58.799999 | 12.852 |


- `volume:issueid:360148977`

| timestamp                  | volume      |
|----------------------------|------------|
| datetime[μs]               | f64        |
| 2023-12-29 09:58:58.800    | 61627.0    |
| 2023-12-29 10:58:58.800    | 83854.0    |
| 2023-12-29 11:58:58.800    | 78240.0    |
| 2023-12-29 12:58:01.200    | 69263.0    |
| 2023-12-29 13:58:58.800    | 59040.0    |
| 2023-12-29 14:58:58.800    | 62831.0    |
| 2023-12-29 15:58:01.200    | 66681.0    |
| 2023-12-29 16:58:58.800    | 529315.0   |
| 2023-12-29 17:34:58.799999 | 1.317919e6 |

- `ohlc:issueid:360148977`

| timestamp           | open   | high   | low    | close  |
|----------------------|--------|--------|--------|--------|
| datetime[μs]         | f64    | f64    | f64    | f64    |
| 2023-12-29 09:00:00 | 12.858 | 12.898 | 12.858 | 12.872 |
| 2023-12-29 10:00:00 | 12.872 | 12.876 | 12.84  | 12.85  |
| 2023-12-29 11:00:00 | 12.85  | 12.864 | 12.842 | 12.848 |
| 2023-12-29 12:00:00 | 12.844 | 12.884 | 12.844 | 12.87  |
| 2023-12-29 13:00:00 | 12.868 | 12.886 | 12.86  | 12.87  |
| 2023-12-29 14:00:00 | 12.872 | 12.902 | 12.868 | 12.886 |
| 2023-12-29 15:00:00 | 12.884 | 12.894 | 12.874 | 12.876 |
| 2023-12-29 16:00:00 | 12.876 | 12.882 | 12.854 | 12.858 |
| 2023-12-29 17:00:00 | 12.856 | 12.858 | 12.83  | 12.852 |


All the models are described in this module :
 - [chart.py](degiro_connector/quotecast/models/chart.py)

For a more comprehensive example :
 - [chart_format.py](examples/quotecast/chart_format.py)

## 2.5. How to find a product `vwd_id` ?

In operations related to `Quotecast`, Degiro uses the `vwd_id` to identify a product.

Which means that if you want a `Chart` or `Real-time data` for a specific product : you first need to find this product's `vwd_id`.

This two identifiers are not the same :

|**Identifier**|**API name(s)**|**Description**|
|:-|:-|:-|
|id|str|Id used identify a product in `Trading` related endpoints.|
|vwd_id|issueid <br /> vwdId <br /> vwdIdSecondary <br />|Id used identify a product in `Quotecast` (`Chart` and `Real-time data`) related endpoint.|

Here are some methods you can use to fetch a product's `vwd_id` :
- `product_search`
- `get_products_info`

The method `product_search` let you use the name or other attributes of a product to fetch it's `vwd_id`.

The method `get_products_info` let you use a product's `id` to fetch it's `vwd_id`.

## 2.6. What are the credentials ?

The only credential you need in order to fetch real-time data and charts is the :
* user_token

Beware, these two identifiers are not the same thing :
* user_token : used to fetch real-time data and charts.
* int_account : used for some trading operations.

## 2.7. How to connect ?

In order to fetch data you need to establish a connection.

You can use the following code to connect :

```python
session_id = TickerFetcher.get_session_id(user_token=YOUR_USER_TOKEN)
```

## 2.8. Is there a timeout ?

Connection timeout is around 15 seconds.

Which means a connection will cease to work after this timeout.

This timeout is reset each time you use this connection to :
* Subscribe to a metric (for instance a stock Price)
* Fetch the data-stream

So if you use it nonstop (in a loop) you won't need to reconnect.

## 2.9. How to subscribe to a data-stream ?

If one needs the following data from the "AAPL" stock :
* LastDate
* LastTime
* LastPrice
* LastVolume

You can use this library to retrieve updates like this :

| product_id    | LastPrice | LastVolume | LastDatetimeUTC         | request_duration_s | response_datetime_utc          |
|---------------|-----------|------------|-------------------------|---------------------|---------------------------------|
| str           | f64       | i64        | datetime[μs]            | f64                 | datetime[μs]                    |
| 360015751     | 34.6      | 1          | 2023-12-29 16:35:23     | 1.021337            | 2024-01-01 17:31:22.482618     |
| AAPL.BATS,E   | 192.55    | null       | 2023-12-29 20:59:59     | 1.021337            | 2024-01-01 17:31:22.482618     |


To subscribe to a data-stream you need to setup a TickerRequest.

A Request has the following parameters :

|**Parameter**|**Type**|**Description**|
|:-|:-|:-|
|request_type|str|The value "subscription" or "unsubscription".|
|request_map|dict|Map of products and metrics to subscribe/unsubscribe to.|

Here is an example of a request :
```python
ticker_request = TickerRequest(
    request_type="subscription",
    request_map={
        "360015751": [
            'LastDate',
            'LastTime',
            'LastPrice',
            'LastVolume',
            'AskPrice',
            'AskVolume',
            'LowPrice',
            'HighPrice',
            'BidPrice',
            'BidVolume'
        ],
        "AAPL.BATS,E": [
            'LastDate',
            'LastTime',
            'LastPrice',
            'LastVolume',
            'AskPrice',
            'AskVolume',
            'LowPrice',
            'HighPrice',
            'BidPrice',
            'BidVolume'
        ],
    },
)
```

In this example these are the `vwd_id` of the products from which you want `Real-time data` :
- 360015751
- AAPL.BATS,E

See the [section](#215-how-to-find-a--vwd_id-) related to `vwd_id` for more information.

Once you have built this Request object you can send it to Degiro's API like this :
```python
TickerFetcher.subscribe(
    ticker_request=ticker_request,
    session_id=session_id,
)
```

For more comprehensive examples :
[realtime_poller.py](examples/quotecast/realtime_poller.py) /
[realtime_one_shot.py](examples/quotecast/realtime_one_shot.py)

## 2.10. How to unsubscribe to a data-stream ?

To remove metrics from the data-stream you need to setup a TickerRequest.

If you try to unsubscribe to a metric to which you didn't subscribed previously it will most likely have no impact.

A Request has the following parameters :

|**Parameter**|**Type**|**Description**|
|:-|:-|:-|
|request_type|str|The value "subscription" or "unsubscription".|
|request_map|dict|Map of products and metrics to subscribe/unsubscribe to.|

Here is an example of a request :
```python
ticker_request = TickerRequest(
    request_type="unsubscription",
    request_map={
        "360015751": [
            'LastDate',
            'LastTime',
            'LastPrice',
            'LastVolume',
            'AskPrice',
            'AskVolume',
            'LowPrice',
            'HighPrice',
            'BidPrice',
            'BidVolume'
        ],
        "AAPL.BATS,E": [
            'LastDate',
            'LastTime',
            'LastPrice',
            'LastVolume',
            'AskPrice',
            'AskVolume',
            'LowPrice',
            'HighPrice',
            'BidPrice',
            'BidVolume'
        ],
    },
)
TickerFetcher.subscribe(
    ticker_request=ticker_request,
    session_id=session_id,
)
```

For more comprehensive examples :
[realtime_poller.py](examples/quotecast/realtime_poller.py) /
[realtime_one_shot.py](examples/quotecast/realtime_one_shot.py)

## 2.11. How to fetch the data ?

You can use the following code :
```python
session_id = TickerFetcher.get_session_id(user_token=user_token)
logger = TickerFetcher.build_logger()
session = TickerFetcher.build_session()
ticker = TickerFetcher.fetch_ticker(
    session_id=session_id,
    session=session,
    logger=logger,
)
```

For a more comprehensive example :
[realtime_poller.py](examples/quotecast/realtime_poller.py)


## 2.12. How to use this data ?

Received data is a `Quotecast` object with the following properties :

|**Parameter**|**Type**|**Description**|
|:-|:-|:-|
|json_data|dict|Dictionary representation of what Degiro's API has sent.|
|metadata|Metadata|Containing the "response_datetime" and "request_duration".|

Here is how to access these properties :
```python
json_text = ticker.json_text
response_datetime = ticker.response_datetime
request_duration= ticker.request_duration
```
Notes: 
* The API sometimes might return an empty Quotecast message.
* The API often returns a subset of the requested metrics, e.g. only `'LastPrice'`. This should be considered when appending consecutive data responses.

## 2.13. Which are the available data types ?

This library provides the tools to convert Degiro's JSON data into something more programmer-friendly.

Here is the list of available data types :

|**Type**|**Description**|
|:-|:-|
|list[Metric]|List of Metric, which is a Pydantic BaseModel.|
|polars.DataFrame|DataFrame from the library Polars.|

There are integrated method to turn `polars.DataFrame` into Python `dict`/`list` or `pandas.DataFrame`.

Here is how to build each type :

```python
# BUILD `LIST[METRIC]`
ticker_to_metric_list = TickerToMetricList()
metric_list = ticker_to_metric_list.parse(ticker=ticker)

# BUILD `POLARS.DATAFRAME`
ticker_to_df = TickerToDF()
polars_df = ticker_to_df.parse(ticker=ticker)

# BUILD `LIST[DICT]`
python_list = polars_df.to_dicts()

# BUILD PANDAS.DATAFRAME
# YOU NEED PANDAS AND PYARROW INSTALLED
pandas_df = df.to_pandas()
```

## 2.14. What is a Ticker ?

The generated Ticker contains :

|**Parameter**|**Type**|**Description**|
|:-|:-|:-|
|json_text|str|The json message received|
|response_datetime|datetime|Datetime of the response.|
|request_duration|timedelta|Duration of the request.|

A Ticker is Pydantic BaseModel, it can serialize and deserialize into json.

Here is how to manipulate a Ticker object :

```python
# GET TICKER PARAMETERS
json_text = ticker.json_text
response_datetime = ticker.response_datetime
request_duration= ticker.request_duration

# SERIALIZE/DESERIALIZE
ticker_json = Ticker.model_dump_json()
ticker_json = Ticker.model_validate_json(json_data=ticker_json)
```

## 2.15. What is inside the `list[Metric]` ?

The `list[Metric]` is the parsed version of the `json` message received from Degiro's API.

A Metric contains the following parameters :

|**Parameter**|**Type**|**Description**|
|:-|:-|:-|
|metric_type|MetricType|str|A metric type like "LastDate", "LastPrice", etc|
|product_id|str|The product identifier in the Quotecast API.|
|value|str|float|The value of the metric.|

Example - `list[Metric]` :

```python
metric_list = [
    Metric(
        product_id=360114899,
        metric_type="LastDate",
        value="2020-11-06",
    ),
    Metric(
        product_id=360114899,
        metric_type="LastTime",
        value="17:36:17",
    ),
    Metric(
        product_id=360114899,
        metric_type="LastPrice",
        value=70.0,
    ),
    Metric(
        product_id=360114899,
        metric_type="LastVolume",
        value=100,
    ),
    Metric(
        product_id=360015751,
        metric_type="LastDate",
        value="2020-11-06",
    ),
    Metric(
        product_id=360015751,
        metric_type="LastTime",
        value="17:36:17",
    ),
    Metric(
        product_id=360015751,
        metric_type="LastPrice",
        value=22.99,
    ),
    Metric(
        product_id=360015751,
        metric_type="LastVolume",
        value=470,
    ),
}
```

## 2.16. What is inside the DataFrame ?

In addition to whatever metrics you have chosen to subscribe to (see the example in [section 2.6](#26-how-to-subscribe-to-a-data-stream-)), the DataFrame will contain the following columns :
|**Column**|**Description**|
|:-|:-|
|product_id|Product identifier, for instance "AAPL.BATS,E" for APPLE stock.|
|response_datetime|Datetime at which the data was received.|
|request_duration|Duration of the request used to fetch the data.|

Example - DataFrame :


| product_id    | LastPrice | LastVolume | LastDatetimeUTC         | request_duration_s | response_datetime_utc          |
|---------------|-----------|------------|-------------------------|---------------------|---------------------------------|
| str           | f64       | i64        | datetime[μs]            | f64                 | datetime[μs]                    |
| 360015751     | 34.6      | 1          | 2023-12-29 16:35:23     | 1.021337            | 2024-01-01 17:31:22.482618     |
| AAPL.BATS,E   | 192.55    | null       | 2023-12-29 20:59:59     | 1.021337            | 2024-01-01 17:31:22.482618     |

# 3. Trading connection

This library is divided into two modules :
- quotecast : to consume real-time financial data.
- trading : to manage your Degiro's account.

The module **quotecast** is described in the section related to real-time data.

The rest of this document will only refer to the module : **trading**.

## 3.1. How to login ?
In order to use the module **trading.api** you need to establish a connection.

Check the section related to **int_account** to understand how to get yours.

Here is how to connect :
```python

credentials = Credentials(
    username = YOUR_USERNAME,
    password = YOUR_PASSWORD,
    int_account = YOUR_INT_ACCOUNT,  # OPTIONAL FOR LOGIN
)

# SETUP TRADING API
trading_api = API(credentials=credentials)

# ESTABLISH CONNECTION
trading_api.connect()
```

For a more comprehensive example :
[connection.py](examples/trading/connection.py)

## 3.2. How to logout ?

Once you no longer need to use the API you can destroy your connection.

You can use the following code to disconnect :

```python
# DESTROY CONNECTION
trading_api.logout()
```

For a more comprehensive example :
[logout.py](examples/trading/logout.py)

## 3.3. What are the credentials ?

Some credentials are required to use Degiro's trading API.

Here are these credentials :

|**Parameter**|**Type**|**Description**|
|:-|:-|:-|
|username|str|Username used to log into Degiro's website.|
|password|str|Password used to log into Degiro's website.|
|int_account|int|OPTIONAL : unique identifier of the account : used by Degiro's server.|
|totp_secret_key|str|OPTIONAL : used for Two-factor Authentication (2FA).|
|one_time_password|str|OPTIONAL : used for Two-factor Authentication (2FA).|

Check the section related to **int_account** to understand how to get yours.

Check the section related to **2FA** if you want to know more about these two parameters :
- **totp_secret_key**
- **one_time_password**

## 3.4. How to find your : int_account ?

To get your **int_acccount** you can run this example :
[client_details_table.py](examples/trading/client_details_table.py)

See section related to **ClientDetails** table for more details.

This **int_acccount** is required to do most of the trading operations available in this connector.

Here are some operations for which your **int_acccount** is not required :
- Connection
- Fetch table : ClientDetails
- Fetch table : Config

Beware, these two identifiers are not the same thing :
- user_token : used to fetch real-time data and charts.
- int_account : used for some trading operations.

## 3.5. How to use 2FA ?

First I will briefly explain what is : **Two-Factor Authentication (2FA)**.

I recommend to skip a few paragraphs if you already know what is **2FA**.

In a standard connection you are providing two parameters:
- username
- password

If you use **Two-Factor Authentication (2FA)** you need an extra parameter:
- one_time_password

This **one_time_password** has a validity of 30 secondes and is generated using a **totp_secret_key** code.

Usually you use an app like **‎Google Authenticator** to store this **totp_secret_key** and generate the **one_time_password**.

The **totp_secret_key** is stored inside the QRCode which is displayed when you enable 2FA on Degiro's website

To use **2FA** with this library you have two solutions.

**SOLUTION 1**

Provide your **totp_secret_key** : the library will use it to generate a new **one_time_password** at each connection.

So you won't have to type your **one_time_password** manually at each connection.

This is the proper way.

See the section about **totp_secret_key** to understand how to get yours.

Here is an example of connection with the **totp_secret_key** :
```python

credentials = Credentials(
    username=YOUR_USERNAME,
    password=YOUR_PASSWORD,
    int_account=YOUR_INT_ACCOUNT,  # OPTIONAL FOR LOGIN
    totp_secret_key=YOUR_2FA_SECRET_KEY,  # ONLY IF 2FA IS ENABLED
)

# SETUP TRADING API
trading_api = API(credentials=credentials)

# ESTABLISH CONNECTION
trading_api.connect()
```

A complete example here :
[connection_2fa.py](examples/trading/connection_2fa.py)

**SOLUTION 2**

Provide a new **one_time_password** at each connection.

Here is an example of connection with the **one_time_password** :
```python

credentials = Credentials(
    username=YOUR_USERNAME,
    password=YOUR_PASSWORD,
    int_account=YOUR_INT_ACCOUNT,  # OPTIONAL FOR LOGIN
    one_time_password=YOUR_2FA_OTP,  # ONLY IF 2FA IS ENABLED
)

# SETUP TRADING API
trading_api = API(credentials=credentials)

# ESTABLISH CONNECTION
trading_api.connect()
```

A complete example here :
[connection_otp.py](examples/trading/connection_otp.py)

## 3.6. How to find your : totp_secret_key ?

The parameter **totp_secret_key** is only required if you have enabled `2FA` on Degiro's website.

When you try to activate `2FA` on Degiro's website, it displays a `QRCode`.

This `QRCode` changes at each activation.

A `QRCode` is a picture which can be converted into a text.

You can download this `QRCode` and use a tool to extract the text from it.

This extracted text will look like this :

    otpauth://totp/DEGIRO:YOUR_USERNAME?algorithm=SHA1&issuer=DEGIRO&secret=YOUR_TOPT_SECRET_KEY&digits=6&period=30

Has you can guess the "totp_secret_key" is in this part :

    secret=YOUR_TOPT_SECRET_KEY

Here is an example of script that extracts the text from a `QRCode` :
[qrcode.py](examples/trading/qrcode.py)

## 3.7. How to find your : one_time_password ?

The parameter **one_time_password** is the password you type when you log in the website using **2FA**.

Usually you get it through an app like **Google Authenticator**.

It is preferable to use the parameter **totp_secret_key** instead of **one_time_password**.

## 3.8. Is there a timeout ?
A connection for trading operations has a timeout of 30 minutes. 
It's [defined](https://github.com/Chavithra/degiro-connector/blob/main/degiro_connector/core/constants/timeouts.py#L2) in seconds as constant `timeouts.TRADING_TIMEOUT`.

The timeout period is started when the [`TradingAPI.connect()`](#31-how-to-login-) results successfully.

Every time an operation is made to this `TradingAPI` connection, the timeout for this connection will be reset.

If a `TradingAPI` connection is left unused during the timeout period, the connection will expire.
Every consecutive function call to the `TraderAPI` will then throw a `TimeoutError` exception.

A connection timeout might occur when your trading strategy only performs a few trades per day, e.g. once per hour.
So when finally a buy opportuntiy occurs, [`check_order()`](#411-check-order):
```python
# FETCH CHECKING_RESPONSE
checking_response = trading_api.check_order(order=order)
```

Will fail with `TimeoutError`:
```
TimeoutError: Connection has probably expired.
```

## 3.9. How to manage : TimeoutError ?

**HANDLE EXCEPTION**

It's recommended to catch the `TimeoutError` on every function call to the `TradingAPI`.

When it's detected, it's sufficient to call [`connect()`](#31-how-to-login-) again, followed by repeating the original call that threw the exception. 
Example for the [`check_order()`](#411-check-order) call:

```python
try:
    checking_response = trading_api.check_order(order=order)
except TimeoutError:
    logging.warning("TradingAPI session did timeout, reconnecting for new session ID...")
    trading_api.connect()
    checking_response = trading_api.check_order(order=order)
```

This shows the following in the log, while the order is checked successfully after a successful reconnect:
```python
WARNING - TradingAPI session did timeout, reconnecting for new session ID...
INFO - get_session_id:response_dict: {'isPassCodeEnabled': False, 'locale': 'nl_NL', 'redirectUrl': 'https://trader.degiro.nl/trader/', 'sessionId': '2BADBBEF3****', 'status': 0, 'statusText': 'success'}
INFO - confirmation_id: "053df7cf-****"
response_datetime {
  seconds: 1643801134
  nanos: 715765000
}
```

**REFRESH TIMEOUT**

As mentioned before, the timeout will be reset after each call to the `TradingAPI`. This provides the opportunity to make a periodic function call, for example every 10 minutes to [`get_update()`](#51-how-to-retrieve-pending-orders-).

However, this might interfere with your other logic and might not be robust over time when DeGiro decides to decrease the timeout on their server.

Therefor it's strongly recommended to always incorporate the exception handling for `TimeoutError` as indicated in the example above.

**CHANGE PERIOD**

It's possible to change the timeout period while creating the `TradingAPI`. Just add a `ModelConnection` object for parameter `connection_storage`:
```python
# SETUP TRADING API
trading_api = TradingAPI(
    credentials=credentials,
    connection_storage=ModelConnection(
        timeout=600,
    )
)

# Connect:
trading_api.connect()
```
The connection will now expire after 10 minutes (10 * 60 s).


# 4. Order

Creating and updating of orders is done with an `Order` object. Here are the parameters:

|**Parameter**|**Type**|**Description**|
|:-|:-|:-|
|id|str|Optional for [`update_order()`](#42-how-to-update-an-order-). It's the `order_id` of the created `Order` as returned by [`confirm_order()`](#412-confirm-order).|
|action|`Order.Action`|Whether you want to : `BUY` or `SELL`.|
|order_type|`Order.OrderType`|Type of order : `LIMIT`, `STOP_LIMIT`, `MARKET` or `STOP_LOSS`.|
|price|float|Limit price of the order. <br /> Optional for the following `order_type` : `LIMIT` and `STOPLIMIT`.|
|product_id|int|Identifier of the product concerned by the order.|
|size|float|Size of the order.|
|stop_price|float|Stop price of the order. <br /> Optional for the following `order_type` : `STOPLIMIT` and `STOPLOSS`|
|time_type|`Order.TimeType`|Duration of the order : `GOOD_TILL_DAY` or `GOOD_TILL_CANCELED`|

The full description of an `Order` is available here :
[order.py](examples/trading/order.py)

## 4.1. How to create an Order ?

The order creation is done in two steps :
1. Checking : send the `Order` to the API to check if it is valid.
2. Confirmation : confirm the creation of the `Order`.

Keeping these two steps (instead of reducing to one single "create" function) provides more options.

## 4.1.1 Check order
Use the `check_order()` function of the Trading API:

### **Request parameters**

|**Parameter**|**Type**|**Description**|
|:-|:-|:-|
|order|`Order`|The order to create with all necessary [parameters](#4-order).|

### **Response parameters**
On a succesfull request, a `dict` with the following parameters is returned:

|**Parameter**|**Type**|**Description**|
|:-|:-|:-|
|confirmation_id|str|Id necessary to confirm the creation of the Order by the [`confirm_order()`](#412-confirm-order) function.|
|response_datetime|datetime|Datetime of the response.|
|free_space_new|float|New free space (balance) if the Order is confirmed.|
|transaction_fees|float|Transaction fees that will be applied to the Order.|
|show_ex_ante_report_link|bool|?|

When the request fails, `None` is returned.

## 4.1.2 Confirm order
Use the `confirm_order()` function of the Trading API:

### **Request parameters**

|**Parameter**|**Type**|**Description**|
|:-|:-|:-|
|confirmation_id|str|The confirmtation id from the [`check_order()`](#411-check-order) response.|
|order|`Order`|The same order from the [`check_order()`](#411-check-order) request.|

### **Response parameters**
On a succesfull request, a `dict` with the following parameters is returned:

|**Parameter**|**Type**|**Description**|
|:-|:-|:-|
|order_id|str|A unique id of the accepted order. This id is required to [update](#42-how-to-update-an-order-) or [delete](#43-how-to-delete-an-order-) the pending order.|
|response_datetime|datetime|Datetime of the response.|

When the request fails, `None` is returned.

## 4.1.3 Example of combining these functions

```python
order = Order(
    buy_sell=Action.BUY,
    order_type=OrderType.LIMIT,
    price=12.1,
    product_id=72160,
    size=1,
    time_type=TimeType.GOOD_TILL_DAY,
)
checking_response = trading_api.check_order(order=order)
confirmation_response = trading_api.confirm_order(
    confirmation_id=checking_response.confirmation_id,
    order=order,
)
```

For a more comprehensive example :
[order.py](examples/trading/order.py)

## 4.2. How to update an Order ?

To modify a specific Order, you need to set it up with the `order_id` from the [`confirm_order()`](#412-confirm-order) response and use the `update_order()` function of the Trading API:

### **Request parameters**

|**Parameter**|**Type**|**Description**|
|:-|:-|:-|
|order|`Order`|The order to update with all necessary [parameters](#4-order), including `id` as returned by [`confirm_order()`](#412-confirm-order).|

### **Response parameters**
On a succesfull request, a `bool` with the value `True` is returned.

When the request fails, `None` is returned. A valid reason is that the pending order has been already executed on the exchange, and this `order_id` no longer exists.

Here is an example:

```python
# ORDER SETUP
order = Order(
    id=YOUR_ORDER_ID,   # `order_id` from `confirm_order()` response
    action=Order.Action.BUY,
    order_type=Order.OrderType.LIMIT,
    price=10.60,
    product_id=71981,
    size=1,
    time_type=Order.TimeType.GOOD_TILL_DAY,
)

# UPDATE ORDER
succcess = trading_api.update_order(order=order)
```

## 4.3. How to delete an Order ?

To delete a specific Order you just need the `order_id` from the [`confirm_order()`](#412-confirm-order) response and use the `delete_order()` function of the Trading API:

### **Request parameters**

|**Parameter**|**Type**|**Description**|
|:-|:-|:-|
|order_id|str|The unique id of the accepted order as returned by [`confirm_order()`](#412-confirm-order).|

### **Response parameters**
On a succesfull request, a `bool` with the value `True` is returned.

When the request fails, `None` is returned. A valid reason is that the pending order has been already executed on the exchange, and this `order_id` no longer exists.

Here is an example:

```python
# DELETE ORDER
succcess = trading_api.delete_order(order_id=YOUR_ORDER_ID) # `order_id` from `confirm_order()` response
```

# 5. Portfolio

## 5.1. How to retrieve pending Orders ?

This is how to get the list of Orders currently created but not yet executed or deleted :
```python
account_update = trading_api.get_update(
    request_list=[
        UpdateRequest(
            option=UpdateOption.ORDERS,
            last_updated=0,
        ),
    ],
    raw=True,
)
```

Example : Orders

       product_id      time_type  price  size                                    id  ...  action  order_type stop_price retained_order  sent_to_exchange
    0           0  GOOD_TILL_DAY      2     3  202cb962-ac59-075b-964b-07152d234b70  ...     BUY       LIMIT         16             17                18

For a more comprehensive example :
[update.py](examples/trading/update.py)

## 5.2. How to get the Portfolio ?

This is how to list the stocks/products currently in the portfolio :
```python
account_update = trading_api.get_update(
    request_list=[
        UpdateRequest(
            option=UpdateOption.PORTFOLIO,
            last_updated=0,
        ),
    ],
    raw=True,
)
```

For a more comprehensive example :
[update.py](examples/trading/update.py)

Note: In order to resolve product IDs to Human readable names, see [7.12. How to search products from ids ?](#712-how-to-search-products-from-ids-)

## 5.3. How to get the TotalPortfolio ?

This is how to get aggregated data about the portfolio :
```python
account_update = trading_api.get_update(
    request_list=[
        UpdateRequest(
            option=UpdateOption.TOTALPORTFOLIO,
            last_updated=0,
        ),
    ],
    raw=True,
)
```

Example : DataFrame

       degiroCash  flatexCash  totalCash  totalDepositWithdrawal  todayDepositWithdrawal  ...  reportNetliq  reportOverallMargin  reportTotalLongVal  reportDeficit  marginCallStatus
    0           0           1          2                       3                       4  ...            16                   17                  18             19    NO_MARGIN_CALL

For a more comprehensive example :
[update.py](examples/trading/update.py)

## 5.4. How to retrieve the OrdersHistory ?

This method returns data about passed orders between two dates.

The result contains a list of "Orders" objects with the following attributes :

|**Parameter**|**Type**|**Description**|
|:-|:-|:-|
|created|str|RFC 3339 Datetime, example : "2020-10-06T20:07:18+02:00".|
|orderId|str|MD5 HASH, example : "098f6bcd-4621-d373-cade-4e832627b4f6"|
|productId|int|Id of the product example : 65156|
|size|float|Size of the order, example : 10.0000|
|price|float|Price of the order, example : 8.6800|
|buysell|str|"B" or "S"|
|orderTypeId|int|see 3.Order|
|orderTimeTypeId|int|see 3.Order|
|stopPrice|float|Price like : 0.0000|
|totalTradedSize|int|-|
|type|str|"CREATE", "DELETE" or "MODIFY"|
|status|str|"CONFIRMED"|
|last|str|RFC 3339 Datetime, example : "2020-10-06T20:07:18+02:00".|
|isActive|bool|-|

Here is how to get this data :

```python
# SETUP REQUEST
orders_history = trading_api.get_orders_history(
    history_request=HistoryRequest(
        from_date=date(year=date.today().year, month=1, day=1),
        to_date=date.today(),
    ),
    raw=True,
)
```

For a more comprehensive example :
[orders_history.py](examples/trading/orders_history.py)

## 5.5. How to retrieve the TransactionsHistory ?

Here is how to get this data :

```python
# SETUP REQUEST
from_date = TransactionsHistory.Request.Date(year=2020,month=11,day=15)
to_date = TransactionsHistory.Request.Date(year=2020,month=10,day=15)
request = TransactionsHistory.Request(from_date=from_date, to_date=to_date)

# FETCH DATA
transactions_history = trading_api.get_transactions_history(request=request)
```

For a more comprehensive example :
[transactions_history.py](examples/trading/transactions_history.py)

## 5.6 How to retrieve Upcoming Payments ?

Here is how to get this data :


```python
# FETCH DATA
upcoming_payments = trading_api.get_upcoming_payments()
```

For a more comprehensive example :
[upcoming_payments.py](examples/trading/upcoming_payments.py)

# 6. Account

## 6.1. How to retrieve the table : Config ?

The config table contains the following informations :

|**Parameter**|**Type**|**Description**|
|:-|:-|:-|
|sessionId|str|Current session id.|
|clientId|int|Unique Degiro's Account identifier also called "userToken"|
|tradingUrl|str|-|
|paUrl|str|-|
|reportingUrl|str|-|
|paymentServiceUrl|str|-|
|productSearchUrl|str|-|
|dictionaryUrl|str|-|
|productTypesUrl|str|-|
|companiesServiceUrl|str|-|
|i18nUrl|str|-|
|vwdQuotecastServiceUrl|str|-|
|vwdNewsUrl|str|-|
|vwdGossipsUrl|str|-|
|taskManagerUrl|str|-|
|refinitivNewsUrl|str|-|
|refinitivAgendaUrl|str|-|
|refinitivCompanyProfileUrl|str|-|
|refinitivCompanyRatiosUrl|str|-|
|refinitivFinancialStatementsUrl|str|-|
|refinitivClipsUrl|str|-|
|landingPath|str|-|
|betaLandingPath|str|-|
|mobileLandingPath|str|-|
|loginUrl|str|-|

Here is how to get this table :

```python
# FETCH DATA
config_table = trading_api.get_config()

# EXTRACT SOME DATA
user_token = config_table['clientId']
session_id = config_table['sessionId']
```

For a more comprehensive example :
[config_table.py](examples/trading/config_table.py)

## 6.2. How to retrieve the table : ClientDetails ?

The ClientDetails table contains information about the current Degiro Account.

|**Parameter**|**Type**|
|:-|:-|
|id|int|
|intAccount|int|
|loggedInPersonId|int|
|clientRole|str|
|effectiveClientRole|str|
|contractType|str|
|username|str|
|displayName|str|
|email|str|
|firstContact.firstName|str|
|firstContact.lastName|str|
|firstContact.displayName|str|
|firstContact.nationality|str|
|firstContact.gender|str|
|firstContact.dateOfBirth|str|
|firstContact.placeOfBirth|str|
|firstContact.countryOfBirth|str|
|address.streetAddress|str|
|address.streetAddressNumber|str|
|address.zip|str|
|address.city|str|
|address.country|str|
|cellphoneNumber|str|
|locale|str|
|language|str|
|culture|str|
|bankAccount.bankAccountId|int|
|bankAccount.bic|str|
|bankAccount.iban|str|
|bankAccount.status|str|
|flatexBankAccount.bic|str|
|flatexBankAccount.iban|str|
|memberCode|str|
|isWithdrawalAvailable|bool|
|isAllocationAvailable|bool|
|isIskClient|bool|
|isCollectivePortfolio|bool|
|isAmClientActive|bool|
|canUpgrade|bool|

Here is how to get this table :

```python
# FETCH DATA
client_details_table = trading_api.get_client_details()

# EXTRACT SOME DATA
int_account = client_details_table['data']['intAccount']
user_token = client_details_table['data']['id']
```

For a more comprehensive example :
[client_details_table.py](examples/trading/client_details_table.py)

## 6.3. How to retrieve the table : AccountInfo ?

The AccountInfo table contains the following information about currencies.

|**Parameter**|**Type**|
|:-|:-|
|clientId|int|
|baseCurrency|str|
|currencyPairs|dict|
|marginType|str|
|cashFunds|dict|
|compensationCapping|float|-|

Here is how to get this table :

```python
account_info_table = trading_api.get_account_info()
```

For a more comprehensive example :
[account_info_table.py](examples/trading/account_info_table.py)

## 6.4. How to get the table : AccountOverview ?

It will provide a list of cash movements.

Here is how to get this data :

```python
account_overview = trading_api.get_account_overview(
    overview_request=OverviewRequest(
        from_date=date(year=date.today().year-1, month=1, day=1),
        to_date=date.today(),
    ),
    raw=False,
)
```

For a more comprehensive example :
[account_overview.py](examples/trading/account_overview.py)

Each cash movement contains this kind of parameters :

|**Parameter**|**Type**|
|:-|:-|
|date|str|
|valueDate|str| 
|id|int| 
|orderId|str| 
|description|str| 
|productId|int|
|currency|str|
|change|float|
|balance|dict| 
|unsettledCash|float|
|total|float|


## 6.5. How to export the table : AccountReport ?

It will export a list of cash movements in a specific format.

Available formats :
- CSV
- HTML
- PDF
- XLS

Here is how to get this content in `CSV` format :

```python
report = trading_api.get_account_report(
    report_request=ReportRequest(
        country="FR",
        lang="fr",
        format=Format.CSV,
        from_date=date(year=date.today().year-1, month=1, day=1),
        to_date=date.today(),
    ),
    raw=False,
)
```

Here are the available parameters for `CashAccountReport.Request` :

|**Parameter**|**Type**|**Description**|
|:-|:-|:-|
|format|CashAccountReport.Format|Wanted format : <br>`CSV`<br>`HTML`<br>`PDF`<br>`XLS`|
|country|str|Country name, like : `FR`|
|lang|int|Language, like : `fr`|
|from_date|CashAccountReport.Request.Date|Events starting after this date.|
|to_date|CashAccountReport.Request.Date|Events before this date.|

Models definitions are available are in this module :
[account.py](degiro_connector/trading/models/account.py)

For a more comprehensive example :
[account_report.py](examples/trading/account_report.py)

## 6.6. How to export the table : PositionReport ?

It will export a list of cash movements in a specific format.

Available formats :
- CSV
- HTML
- PDF
- XLS

Here is how to get this content in `CSV` format :

```python
# SETUP REQUEST
report = trading_api.get_position_report(
    report_request=ReportRequest(
        country="FR",
        lang="fr",
        format=Format.XLS,
        from_date=date(year=date.today().year-1, month=1, day=1),
        to_date=date.today(),
    ),
    raw=False,
)
```

Here are the available parameters for `PositionReport.Request` :

|**Parameter**|**Type**|**Description**|
|:-|:-|:-|
|format|PositionReport.Format|Wanted format : <br>`CSV`<br>`HTML`<br>`PDF`<br>`XLS`|
|country|str|Country name, like : `FR`|
|lang|int|Language, like : `fr`|
|to_date|PositionReport.Request.Date|Events before this date.|

Models definitions are available are in this module :
[account.py](degiro_connector/trading/models/account.py)

For a more comprehensive example :
[position_report.py](examples/trading/position_report.py)

# 7. Products

## 7.1. How to get the table : ProductsConfig ?

This table contains useful parameters to filter products.

Here are the parameters which are inside this table :

|**Parameter**|**Type**|
|:-|:-|
|stockCountries|list|
|bondExchanges|list|
|bondIssuerTypes|list|
|eurexCountries|list|
|futureExchanges|list|
|optionExchanges|list|
|combinationExchanges|list|
|cfdExchanges|list|
|exchanges|list|
|indices|list|
|regions|list|
|countries|list|
|productTypes|list|
|etfFeeTypes|list|
|investmentFundFeeTypes|list|
|optionAggregateTypes|list|
|leveragedAggregateTypes|list|
|etfAggregateTypes|list|
|investmentFundAggregateTypes|list|
|lookupSortColumns|list|
|stockSortColumns|list|
|bondSortColumns|list|
|cfdSortColumns|list|
|etfSortColumns|list|
|futureSortColumns|list|

Here is how to get this data :

```python
# FETCH DATA
products_config = trading_api.get_products_config()
```

For a more comprehensive example :
[products_config.py](examples/trading/products_config.py)

## 7.2. How to lookup products (search by name) ?

Text research on a financial product.

Here is how to get this data :

```python
product_request = LookupRequest(
    search_text='APPLE',
    limit=10,
    offset=0,
    product_type_id=1,
)
products_lookup = trading_api.product_search(product_request=product_request)
```

For a more comprehensive example :
[product_lookup.py](examples/trading/product_lookup.py)

## 7.3. How to search bonds ?

Here is how to get this data :

```python
# SETUP REQUEST
product_request = BondsRequest(
    bond_issuer_type_id=0,
    bond_exchange_id=710,

    search_text='',
    offset=0,
    limit=100,
    require_total=True,
    sort_columns='name',
    sort_types='asc',
)

# FETCH DATA
bond_list = trading_api.product_search(product_request=product_request)
```

For a more comprehensive example :
[product_search.py](examples/trading/product_search.py)

## 7.4. How to search etfs ?

Here is how to get this data :

```python
# SETUP REQUEST
product_request = ETFsRequest(
    popular_only=False,
    input_aggregate_types='',
    input_aggregate_values='',

    search_text='',
    offset=0,
    limit=100,
    require_total=True,
    sort_columns='name',
    sort_types='asc',
)

# FETCH DATA
etf_list = trading_api.product_search(product_request=product_request)
```

For a more comprehensive example :
[product_search.py](examples/trading/product_search.py)

## 7.5. How to search funds ?

Here is how to get this data :

```python
# SETUP REQUEST
product_request = FundsRequest(
    search_text='',
    offset=0,
    limit=100,
    require_total=True,
    sort_columns='name',
    sort_types='asc',
)

# FETCH DATA
fund_list = trading_api.product_search(product_request=product_request)
```

For a more comprehensive example :
[product_search.py](examples/trading/product_search.py)

## 7.6. How to search futures ?

Here is how to get this data :

```python
# SETUP REQUEST
product_request = FuturesRequest(
    future_exchange_id=1,
    underlying_isin='FR0003500008',

    search_text='',
    offset=0,
    limit=100,
    require_total=True,
    sort_columns='name',
    sort_types='asc',
)

# FETCH DATA
fund_list = trading_api.product_search(product_request=product_request)
```

For a more comprehensive example :
[product_search.py](examples/trading/product_search.py)

## 7.7. How to search leverageds ?

Here is how to get this data :

```python
# SETUP REQUEST
product_request = LeveragedsRequest(
    popular_only=False,
    input_aggregate_types='',
    input_aggregate_values='',

    search_text='',
    offset=0,
    limit=100,
    require_total=True,
    sort_columns='name',
    sort_types='asc',
)

# FETCH DATA
etf_list = trading_api.product_search(product_request=product_request)
```

For a more comprehensive example :
[product_search.py](examples/trading/product_search.py)

## 7.8. How to search options ?
Here is how to get this data :

```python
# SETUP REQUEST
product_request = OptionsRequest(
    input_aggregate_types='',
    input_aggregate_values='',
    option_exchange_id=3,
    underlying_isin='FR0003500008',

    search_text='',
    offset=0,
    limit=100,
    require_total=True,
    sort_columns='expirationDate,strike',
    sort_types='asc,asc',
)

# FETCH DATA
option_list = trading_api.product_search(product_request=product_request)
```

For a more comprehensive example :
[product_search.py](examples/trading/product_search.py)

## 7.9. How to search stocks ?

It contains information about available stocks.

Here is how to get this data :

```python
# SETUP REQUEST
product_request = StocksRequest(
    index_id=122001,    # NASDAQ 100
    # exchange_id=663,  # NASDAQ
                        # You can either use `index_id` or `exchange id`
                        # See which one to use in the `ProductsConfig` table
    is_in_us_green_list=True,
    stock_country_id=846, # US

    search_text='',
    offset=0,
    limit=100,
    require_total=True,
    sort_columns='name',
    sort_types='asc',
)

# FETCH DATA
stock_list = trading_api.product_search(product_request=product_request)
```

For a more comprehensive example :
[product_search.py](examples/trading/product_search.py)

## 7.10. How to search warrants ?

Here is how to get this data :

```python
# SETUP REQUEST
product_request = WarrantsRequest(
    search_text='',
    offset=0,
    limit=100,
    require_total=True,
    sort_columns='name',
    sort_types='asc',
)

# FETCH DATA
warrant_list = trading_api.product_search(product_request=product_request)
```

For a more comprehensive example :
[product_search.py](examples/trading/product_search.py)

## 7.11. How to search products from ids ?

Here is how to get this data :

```python
product_info = trading_api.get_products_info(
    product_list=[96008, 1153605, 5462588],
    raw=False,
)
```

For a more comprehensive example :
[products_info.py](examples/trading/products_info.py)

## 7.12. How to get my favorite products ?

Here is how to get this data :

```python
favorites_batch = trading_api.get_favorite()
```

For a more comprehensive example :
[favorite_get.py](examples/trading/favorite_get.py)

## 7.13. How to create a favorite list ?

Example :

```python
favorite_id = trading_api.create_favorite(name="SOME_NAME")
```

For a more comprehensive example :
[favorite_create.py](examples/trading/favorite_create.py)

## 7.14. How to delete a favorite list ?

Example :

```python
success = trading_api.delete_favorite(id=1234567)
```

For a more comprehensive example :
[favorite_delete.py](examples/trading/favorite_delete.py)

## 7.15. How to move a favorite list ?

Example :

```python
success = trading_api.move_favorite(
    list_id=1234567,
    position=1,
)
```

For a more comprehensive example :
[favorite_move.py](examples/trading/favorite_move.py)

## 7.16. How to put favorite list products ?

Example :

```python
success = trading_api.put_favorite_product(
    id=1234567,
    product_id=1234567,
)
```

For a more comprehensive example :
[favorite_put_product.py](examples/trading/favorite_put_product.py)

## 7.17. How to delete favorite list products ?

Example :

```python
success = trading_api.delete_favorite_product(
    id=1234567,
    product_id=1234567,
)
```

For a more comprehensive example :
[favorite_delete product.py](examples/trading/favorite_delete product.py)


## 7.18. How to get futures/options underlyings ?

Example :

```python
underlying_list = trading_api.get_underlyings(
    underlyings_request= UnderlyingsRequest(
        future_exchange_id=1,
        # option_exchange_id=3,
    ),
    raw=False,
)
```

For a more comprehensive example :
[favorite_get_underlyings.py](examples/trading/favorite_get_underlyings.py)

# 8. Companies

## 8.1. How to get : CompanyProfile ?

Here is how to get this data :

```python
# FETCH DATA
company_profile = trading_api.get_company_profile(
    product_isin='FR0000131906',
)
```

For a more comprehensive example :
[company_profile.py](examples/trading/company_profile.py)

## 8.2. How to get : CompanyRatios ?

This table contains information about the company.

Here are the parameters which are inside this table :

|**Parameter**|**Type**|
|:-|:-|
|totalFloat|str|
|sharesOut|str|
|consRecommendationTrend|dict|
|forecastData|dict|
|currentRatios|dict|

Here is how to get this data :

```python
# FETCH DATA
company_ratios = trading_api.get_company_ratios(
    product_isin='FR0000131906',
)
```

For a more comprehensive example :
[company_ratios.py](examples/trading/company_ratios.py)

## 8.3. How to get : FinancialStatements ?

Here is how to get this data :

```python
# FETCH DATA
financials_statements = trading_api.get_financials_statements(
    product_isin='FR0000131906',
)
```

For a more comprehensive example :
[financial_statements.py](examples/trading/financial_statements.py)

## 8.4. How to get : LatestNews ?

Here is how to get this data :

```python
# SETUP REQUEST
request = LatestNews.Request(
    offset=0,
    languages='en,fr',
    limit=20,
)

# FETCH DATA
latest_news = trading_api.get_latest_news(
    request=request,
    raw=True,
)
```

For a more comprehensive example :
[latest_news.py](examples/trading/latest_news.py)

## 8.5. How to get : TopNewsPreview ?

Here is how to get this data :

```python
# FETCH DATA
top_news_preview = trading_api.get_top_news_preview(raw=True)
```

For a more comprehensive example :
[top_news_preview.py](examples/trading/top_news_preview.py)

## 8.6. How to get : NewsByCompany ?

Here is how to get this data :

```python
# SETUP REQUEST
request = NewsByCompany.Request(
    isin='NL0000235190',
    limit=10,
    offset=0,
    languages='en,fr',
)

# FETCH DATA
news_by_company = trading_api.get_news_by_company(
    request=request,
    raw=True,
)
```

For a more comprehensive example :
[news_by_company.py](examples/trading/news_by_company.py)


## 8.7. How to get : Agenda ?

Here is how to get this data :

```python
agenda = trading_api.get_agenda(
    agenda_request=AgendaRequest(
        calendar_type=CalendarType.EARNINGS_CALENDAR,
        end_date=datetime.now(),
        start_date=datetime.now() - timedelta(days=1),
        offset=0,
        limit=25,
    ),
    raw=True,
)
```

Here are the available parameters for `Agenda.Request` :

|**Parameter**|**Type**|**Description**|
|:-|:-|:-|
|calendar_type|Agenda.CalendarType|Type of agenda : <br>`DIVIDEND_CALENDAR`<br>`ECONOMIC_CALENDAR`<br>`EARNINGS_CALENDAR`<br>`HOLIDAY_CALENDAR`<br>`IPO_CALENDAR`<br>`SPLIT_CALENDAR`|
|offset|int|-|
|limit|int|-|
|order_by_desc|bool|-|
|start_date|Timestamp|Events starting after this date.|
|end_date|Timestamp|Events before this date.|
|company_name|str|Filter used on the events description.|
|countries|str|Comma separated list of countries like : `FR,US`|
|classifications|str|Comma separated list of sectors like : `GovernmentSector,ExternalSector`|
|units|str|Comma separated list of units like : `Acre,Barrel`|

Exact definitions of `Agenda` and `AgendaRequest` are in this module :
[agenda.py](degiro_connector/trading/models/agenda.py)

For a more comprehensive example :
[agenda.py](examples/trading/agenda.py)


## 8.8. How to get : EstimatesSummaries ?
Here is how to get this data :

```python
estimates_summaries = trading_api.get_estimates_summaries(
    product_isin="FR0000131906",
    raw=False,
)
```

Here are the available parameters for `Agenda.Request` :

|**Parameter**|**Type**|**Description**|
|:-|:-|:-|
|annual|dict|Indicators by year.|
|currency|str|currency, example `EUR`.|
|interim|dict|Indicators by quarter.|
|lastRetrieved|str|Last Retrieved, example : `2021-12-31T20:07:30.939Z`.|
|lastUpdated|str|Last updated,, example : `2021-02-18T01:30:00Z`.|
|preferredMeasure|str|Preferred measure, example : `EPS`.|
|ric|str|Reuters Instrument Code, example : `BOUY.PA`.|

Exact definition of `EstimatesSummaries` is in this file :
[product.py](degiro_connector/trading/models/product.py)

For a more comprehensive example :
[estimates_summaries.py](examples/trading/estimates_summaries.py)

# 9. License
[BSD-3-Clause License](https://raw.githubusercontent.com/Chavithra/degiro-connector/main/LICENSE)
