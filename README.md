# 1. **Degiro Connector**

This is yet another library to access Degiro's API.

Notes :
- Migration scripts are available :
```bash
python -m degiro_connector.migration.from_0_1_3_to_1_0_0
python -m degiro_connector.migration.from_1_0_4_to_1_0_5
python -m degiro_connector.migration.from_1_0_10_to_2_0_0
python -m degiro_connector.migration.from_2_0_2_to_2_0_3
```
- `GRPC` services are available to let you consume this library through other languages like Javascript, Java, Go, C++, Rust, etc :
```bash
python -m examples.quotecast.relay_server
python -m examples.trading.relay_server

```

## 1.1. Which features ?
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
|Favourites|Retrieve favorite products lists.|
|FinancialStatements|Retrieve a company's financial statements using its ISIN code.|
|LatestNews|Retrieve latest news about all the companies.|
|LoginQuotecast|Establish a connection for quotecast operations.|
|LoginTrading|Establish a connection for trading operations.|
|LogoutTrading|Destroy previously established connection for trading operations.|
|NewsByCompany|Retrieve news related to a specific company.|
|Order|Create, update, delete an Order.|
|OrderHistory|Retrieve all Orders created between two dates.|
|Orders|List pending Orders.|
|Portoflio|List products in your Portoflio.|
|ProductsConfig|Retrieve a table containing : useful parameters to filter products.|
|ProductsInfo|Search for products using their ids.|
|Quotecasts|Fetch real-time data on financial products. <br> For instance the real-time stock Price.|
|TopNewsPreview|Retrieve some news preview about all the companies.|
|TotalPorfolio|Retrieve aggregated information about your assets.|
|TransactionsHistory|Retrieve all Transactions created between two dates.|

## 1.2. How to install ?

```bash
pip install degiro-connector
```

## 1.3. How to upgrade ?

```bash
pip install --no-cache-dir --upgrade degiro-connector
```

## 1.4. How to uninstall ?

```bash
pip uninstall degiro-connector
```

## 1.5. Table of contents
- [1. **Degiro Connector**](#1-degiro-connector)
  * [1.1. Which features ?](#11-which-features-)
  * [1.2. How to install ?](#12-how-to-install-)
  * [1.3. How to upgrade ?](#13-how-to-upgrade-)
  * [1.4. How to uninstall ?](#14-how-to-uninstall-)
  * [1.5. Table of contents](#15-table-of-contents)
- [2. Real-time data](#2-real-time-data)
  * [2.1. What are the workflows ?](#21-what-are-the-workflows-)
  * [2.2. What are the credentials ?](#22-what-are-the-credentials-)
  * [2.3. How to find your : user_token ?](#23-how-to-find-your--user_token-)
  * [2.4. How to login ?](#24-how-to-login-)
  * [2.5. Is there a timeout ?](#25-is-there-a-timeout-)
  * [2.6. How to subscribe to a data-stream ?](#26-how-to-subscribe-to-a-data-stream-)
  * [2.7. How to unsubscribe to a data-stream ?](#27-how-to-unsubscribe-to-a-data-stream-)
  * [2.8. How to fetch the data ?](#28-how-to-fetch-the-data-)
  * [2.9. How to use this data ?](#29-how-to-use-this-data-)
  * [2.10. Which are the available data types ?](#210-which-are-the-available-data-types-)
  * [2.11. What is a Ticker ?](#211-what-is-a-ticker-)
  * [2.12. What is inside the Dictionary ?](#212-what-is-inside-the-dictionary-)
  * [2.13. What is inside the DataFrame ?](#213-what-is-inside-the-dataframe-)
  * [2.14. How to get chart data ?](#214-how-to-get-chart-data-)
  * [2.15. How to find a : vwd_id ?](#215-how-to-find-a--vwd_id-)
- [3. Trading connection](#3-trading-connection)
  * [3.1. How to login ?](#31-how-to-login-)
  * [3.2. How to logout ?](#32-how-to-logout-)
  * [3.3. What are the credentials ?](#33-what-are-the-credentials-)
  * [3.4. How to find your : int_account ?](#34-how-to-find-your--int_account-)
  * [3.5. How to use 2FA ?](#35-how-to-use-2fa-)
  * [3.6. How to find your : totp_secret_key ?](#36-how-to-find-your--totp_secret_key-)
  * [3.7. How to find your : one_time_password ?](#37-how-to-find-your--one_time_password-)
  * [3.8. Is there a timeout ?](#38-is-there-a-timeout-)
- [4. Order](#4-order)
  * [4.1. How to create an Order ?](#41-how-to-create-an-order-)
  * [4.2. How to update an Order ?](#42-how-to-update-an-order-)
  * [4.3. How to delete an Order ?](#43-how-to-delete-an-order-)
- [5. Portfolio](#5-portfolio)
  * [5.1. How to retrieve pending Orders ?](#51-how-to-retrieve-pending-orders-)
  * [5.2. How to get the Portfolio ?](#52-how-to-get-the-portfolio-)
  * [5.3. How to get the TotalPortfolio ?](#53-how-to-get-the-totalportfolio-)
  * [5.4. How to retrieve the OrdersHistory ?](#54-how-to-retrieve-the-ordershistory-)
  * [5.5. How to retrieve the TransactionsHistory ?](#55-how-to-retrieve-the-transactionshistory-)
- [6. Account](#6-account)
  * [6.1. How to retrieve the table : Config ?](#61-how-to-retrieve-the-table--config-)
  * [6.2. How to retrieve the table : ClientDetails ?](#62-how-to-retrieve-the-table--clientdetails-)
  * [6.3. How to retrieve the table : AccountInfo ?](#63-how-to-retrieve-the-table--accountinfo-)
  * [6.4. How to get the table : AccountOverview ?](#64-how-to-get-the-table--accountoverview-)
  * [6.5. How to export the table : CashAccountReport ?](#65-how-to-export-the-table--cashaccountreport-)
- [7. Products](#7-products)
  * [7.1. How to get the table : ProductsConfig ?](#71-how-to-get-the-table--productsconfig-)
  * [7.2. How to get my favourite products ?](#72-how-to-get-my-favourite-products-)
  * [7.3. How to lookup products (search by name) ?](#73-how-to-lookup-products-search-by-name-)
  * [7.4. How to search bonds ?](#74-how-to-search-bonds-)
  * [7.5. How to search etfs ?](#75-how-to-search-etfs-)
  * [7.6. How to search funds ?](#76-how-to-search-funds-)
  * [7.7. How to search futures ?](#77-how-to-search-futures-)
  * [7.8. How to search leverageds ?](#78-how-to-search-leverageds-)
  * [7.9. How to search options ?](#79-how-to-search-options-)
  * [7.10. How to search stocks ?](#710-how-to-search-stocks-)
  * [7.11. How to search warrants ?](#711-how-to-search-warrants-)
  * [7.12. How to search products from ids ?](#712-how-to-search-products-from-ids-)
- [8. Companies](#8-companies)
  * [8.1. How to get : CompanyProfile ?](#81-how-to-get--companyprofile-)
  * [8.2. How to get : CompanyRatios ?](#82-how-to-get--companyratios-)
  * [8.3. How to get : FinancialStatements ?](#83-how-to-get--financialstatements-)
  * [8.4. How to get : LatestNews ?](#84-how-to-get--latestnews-)
  * [8.5. How to get : TopNewsPreview ?](#85-how-to-get--topnewspreview-)
  * [8.6. How to get : NewsByCompany ?](#86-how-to-get--newsbycompany-)
  * [8.7. How to get : Agenda ?](#87-how-to-get--agenda-)
- [9. Contributing](#9-contributing)
- [10. License](#10-license)

# 2. Real-time data

It is possible to fetch a stream of data in real-time from Degiro's API.

For instance if one needs the following data from the "AAPL" stock :
* LastDate
* LastTime
* LastPrice
* LastVolume

You can use this library to retrieve updates like this :

    LastDate    LastTime    LastPrice LastVolume
    2020-11-13  22:00:00    119.26    4697040

For a list of available metrics, see the example in [section 2.6](#26-how-to-subscribe-to-a-data-stream-).

## 2.1. What are the workflows ?

This is the workflow for consuming real-time data-stream :

    A. Find your "user_token".
    B. Setup the API object with your "user_token".
    C. Connect.
    D. Subscribe to data-stream.
    E. Fetch data-stream.

This is the worflow for consuming charts :

    A. Find your "user_token".
    B. Setup the API object with your "user_token".
    C. Fetch charts.

All the details of these steps are explained in the rest of this section.

## 2.2. What are the credentials ?

The only credential you need in order to fetch real-time data and charts is the :
* user_token

Beware, these two identifiers are not the same thing :
* user_token : used to fetch real-time data and charts.
* int_account : used for some trading operations.

## 2.3. How to find your : user_token ?
You can find your "user_token" inside one of these tables :
* "Config" : attribute "clientId"
* "ClientDetails" : attribute "id"

See sections related to ["Config"](#61-how-to-retrieve-the-table--config-) and ["ClientDetails"](#62-how-to-retrieve-the-table--clientdetails-) tables.

## 2.4. How to login ?

In order to fetch data you need to establish a connection.

You can use the following code to connect :

```python
# SETUP QUOTECAST API
quotecast_api = API(user_token=YOUR_USER_TOKEN)

# CONNECTION
quotecast_api.connect()
```

## 2.5. Is there a timeout ?

Connection timeout is around 15 seconds.

Which means a connection will cease to work after this timeout.

This timeout is reset each time you use this connection to :
* Subscribe to a metric (for instance a stock Price)
* Fetch the data-stream

So if you use it nonstop (in a loop) you won't need to reconnect.

## 2.6. How to subscribe to a data-stream ?

To subscribe to a data-stream you need to setup a Request message.

A Request has the following parameters :

|**Parameter**|**Type**|**Description**|
|:-|:-|:-|
|subscriptions|MessageMap|List of products and metrics to subscribe to.|
|unsubscriptions|MessageMap|List of products and metrics to unsubscribe to.|

Here is an example of a request :
```python
request = Quotecast.Request()
request.subscriptions['360015751'].extend([
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
])
request.subscriptions['AAPL.BATS,E'].extend([
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
])
```

In this example these are the `vwd_id` of the products from which you want `Real-time data` :
- 360015751
- AAPL.BATS,E

See the [section](#215-how-to-find-a--vwd_id-) related to `vwd_id` for more information.

Once you have built this Request object you can send it to Degiro's API like this :
```python
quotecast_api.subscribe(request=request)
```

For more comprehensive examples :
[realtime_poller.py](examples/quotecast/realtime_poller.py) /
[realtime_one_shot.py](examples/quotecast/realtime_one_shot.py)

## 2.7. How to unsubscribe to a data-stream ?

To remove metrics from the data-stream you need to setup a Request message.

If you try to unsubscribe to a metric to which you didn't subscribed previously it will most likely have no impact.

A Request has the following parameters :
|**Parameter**|**Type**|**Description**|
|:-|:-|:-|
|subscriptions|MessageMap|List of products and metrics to subscribe to.|
|unsubscriptions|MessageMap|List of products and metrics to unsubscribe to.|

Here is an example of a request :
```python
request = Quotecast.Request()
request.unsubscriptions['360015751'].extend([
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
])
request.unsubscriptions['AAPL.BATS,E'].extend([
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
])
```

Once you have built this Request object you can send it to Degiro's API like this :
```python
quotecast_api.subscribe(request=request)
```

For more comprehensive examples :
[realtime_poller.py](examples/quotecast/realtime_poller.py) /
[realtime_one_shot.py](examples/quotecast/realtime_one_shot.py)

## 2.8. How to fetch the data ?

You can use the following code :
```python
quotecast = quotecast_api.fetch_data()
```

For a more comprehensive example :
[realtime_poller.py](examples/quotecast/realtime_poller.py)

## 2.9. How to use this data ?

Received data is a `Quotecast` object with the following properties :

|**Parameter**|**Type**|**Description**|
|:-|:-|:-|
|json_data|dict|Dictionary representation of what Degiro's API has sent.|
|metadata|Metadata|Containing the "response_datetime" and "request_duration".|

Here is how to access these properties :
```python
json_data = quotecast.json_data
response_datetime = quotecast.metadata.response_datetime
request_duration= quotecast.metadata.request_duration
```
Notes: 
* The API sometimes might return an empty Quotecast object.
* The API often returns a subset of the requested metrics, e.g. only `'LastPrice'`. Please take this into account when appending consecutive data responses.

## 2.10. Which are the available data types ?

This library provides the tools to convert Degiro's JSON data into something more programmer-friendly.

Here is the list of available data types :

|**Type**|**Description**|
|:-|:-|
|Ticker|Protobuf message (for GRPC).|
|Dictionaries|Standard Python Dictionaries : **dict**.|
|DataFrame|DataFrame from the library Pandas.|

Here is how to build each type :

```python
# UPDATE PARSER
quotecast_parser.put_quotecast(quotecast=quotecast)

# BUILD TICKER
ticker = quotecast_parser.ticker

# BUILD DICT
ticker_dict = quotecast_parser.ticker_dict

# BUILD PANDAS.DATAFRAME
ticker_df = quotecast_parser.ticker_df
```

## 2.11. What is a Ticker ?

The generated Ticker contains :

|**Parameter**|**Type**|**Description**|
|:-|:-|:-|
|metadata|Metadata|Containing the "response_datetime" and "request_duration".|
|products|MessageMap|Dictionary like object containing the metrics group by "vwd_id".|
|product_list|RepeatedScalarFieldContainer|List of available "vwd_id".|

Here are some operations available :

```python
product = '360015751'
metric_name = 'LastPrice'

# ACCESS SPECIFIC PRODUCT
product = ticker.products[product]

# ACCESS SPECIFIC METRIC
metric = product[metric_name]

# LOOP OVER PRODUCTS
for product in ticker.products:
    product = ticker.products[product]

# LOOP OVER METRICS
for metric_name in product.metrics:
    metric = product.metrics[metric_name]
```

A Ticker is a custom Protocol Buffer Message built for this library.

It can be transmitted over GRPC framework.

## 2.12. What is inside the Dictionary ?

The dictionary representation of a ticker contains the metrics grouped by "vwd_id" (product id), with :
* keys : vwd_id
* values : another dictionary with the metrics concerning this specific product.

Example - Dictionary :

```python
{
    '360114899': {
        'vwd_id': 360114899,
        'response_datetime': '2020-11-08 12:00:27',
        'request_duration': 1.0224891666870117,
        'LastDate': '2020-11-06',
        'LastTime': '17:36:17',
        'LastPrice': '70.0',
        'LastVolume': '100'
    },
    '360015751': {
        'vwd_id': 360015751,
        'response_datetime': '2020-11-08 12:00:27',
        'request_duration': 1.0224891666870117,
        'LastDate': '2020-11-06',
        'LastTime': '17:36:17',
        'LastPrice': '22.99',
        'LastVolume': '470'
    }
}
```

## 2.13. What is inside the DataFrame ?

In addition to whatever metrics you have chosen to subscribe to (see the example in [section 2.6](#26-how-to-subscribe-to-a-data-stream-)), the DataFrame will contain the following columns :
|**Column**|**Description**|
|:-|:-|
|vwd_id|Product identifier, for instance "AAPL.BATS,E" for APPLE stock.|
|response_datetime|Datetime at which the data was received.|
|request_duration|Duration of the request used to fetch the data.|

Example - DataFrame :

           vwd_id    response_datetime  request_duration    LastDate  LastTime LastPrice LastVolume
    0   360114899  2020-11-08 12:00:27          1.022489  2020-11-06  17:39:57      70.0        100
    1   360015751  2020-11-08 12:00:27          1.022489  2020-11-06  17:36:17     22.99        470

## 2.14. How to get chart data ?
You can fetch an object containing the same data than in Degiro's website graph.

For that you need to prepare a Chart.Request object.

Here is a table with the available attributes for Chart.Request.

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
request = Chart.Request()
request.culture = "fr-FR"
request.period = Chart.Interval.PT1H
request.requestid = "1"
request.resolution = Chart.Interval.P1D
# request.series.append("issueid:360148977")
# request.series.append("price:issueid:360148977")
request.series.append("ohlc:issueid:360148977")
# request.series.append("volume:issueid:360148977")
# request.series.append("vwdkey:AAPL.BATS,E")
# request.series.append("price:vwdkey:AAPL.BATS,E")
# request.series.append("ohlc:vwdkey:AAPL.BATS,E")
# request.series.append("volume:vwdkey:AAPL.BATS,E")
request.tz = "Europe/Paris"

# FETCH DATA
chart = quotecast_api.get_chart(
    request=request,
    override={
        "resolution": "P1D",
        "period": "P1W",
    },
    raw=True,
)
```

The `issueid` parameter is the `vwd_id` of the product from which you want the `Chart` data.

See the section related to `vwd_id` for more information.

All the options for the enumerations are available in this file :
[quotecast.proto](protos/degiro_connector/quotecast/models/quotecast.proto)

For a more comprehensive examples :
 - [chart.py](examples/quotecast/chart.py)
 - [chart_format.py](examples/quotecast/chart_format.py)

## 2.15. How to find a : vwd_id ?

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
# SETUP CREDENTIALS
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
quotecast_api.logout()
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

In a standard connection you are providing two parameters :
- username
- password

If you use **Two-Factor Authentication (2FA)** you need an extra parameter :
- one_time_password

This **one_time_password** has a validity of 30 secondes and is generated using a **totp_secret_key** code.

This **totp_secret_key** code is provided in Degiro's website when you enable **2FA** : it is the QRCode.

Usually you put this QRCode inside an app like **‎Google Authenticator**.

**‎Google Authenticator** generates a **one_time_password** that you can to log in. 

To use **2FA** with this library you have two solution.

**SOLUTION 1**

Provide your **totp_secret_key** : the library will use it to generate a new **one_time_password** at each connection.

So you won't have to type your **one_time_password** manually at each connection.

This is the proper way.

See the section about **totp_secret_key** to understand how to get yours.

Here is an example of connection with the **totp_secret_key** :
```python
# SETUP CREDENTIALS
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
# SETUP CREDENTIALS
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
A connection for trading operations seems to have a timeout of : around 30 minutes.

If a connection is left unused for this amount of time it will cease to work.

Every time you do an operation using a connection, Degiro's API seems to reset the timeout for this connection.

# 4. Order

Here are the main parameters of an Order.

|**Parameter**|**Type**|**Description**|
|:-|:-|:-|
|action|Order.Action|Whether you want to : `BUY` or `SELL`.|
|order_type|Order.OrderType|Type of order : `LIMIT`, `STOP_LIMIT`, `MARKET` or `STOP_LOSS`.|
|price|float|Price of the order. <br /> Only used for the following `order_type` : `LIMIT` and `STOPLIMIT`.|
|product_id|int|Identifier of the product concerned by the order.|
|size|float|Size of the order.|
|stop_price|float|Stop price of the order. <br /> Only used for the following `order_type` : `STOPLIMIT` and `STOPLOSS`|
|time_type|Order.TimeType|Duration of the order : GOOD_TILL_DAY or GOOD_TILL_CANCELED|

The full description of an Order is available here :
[trading.proto](protos/degiro_connector/trading/models/trading.proto)

## 4.1. How to create an Order ?

The Order creation is done in two step :
* Checking : send the Order to the API to check if it is valid.
* Confirmation : confirm the creation of the Order.

Keeping these two steps (instead of reducing to one single "create" function) provides more options.

Here are the parameters of a CheckingResponse :

|**Parameter**|**Type**|**Description**|
|:-|:-|:-|
|confirmation_id|str|Id necessary to confirm the creation of the Order.|
|free_space_new|float|New free space (balance) if the Order is confirmed.|
|response_datetime|Timestamp|Timestamp can be converted to date string using : ToJsonString().|
|transaction_fees|repeated Struct|Transaction fees that will be applied to the Order.|
|transaction_opposite_fees|repeated Struct|Other kind of fees that will be applied to the Order.|
|transaction_taxes|repeated Struct|Taxes that will be applied to the Order.|

Here are the parameters of a ConfirmationResponse :

|**Parameter**|**Type**|**Description**|
|:-|:-|:-|
|order_id|str|Id of the created Order.|
|response_datetime|Timestamp|Timestamp can be converted to date string using : ToJsonString().|

Here is an example :

```python
# SETUP ORDER
order = Order(
    action=Order.Action.BUY,
    order_type=Order.OrderType.LIMIT,
    price=10,
    product_id=71981,
    size=1,
    time_type=Order.TimeType.GOOD_TILL_DAY,
)

# FETCH CHECKING_RESPONSE
checking_response = trading_api.check_order(order=order)

# EXTRACT CONFIRMATION_ID
confirmation_id = checking_response.confirmation_id

# SEND CONFIRMATION
confirmation_response = trading_api.confirm_order(
    confirmation_id=confirmation_id,
    order=order,
)
```

For a more comprehensive example :
[order.py](examples/trading/order.py)

## 4.2. How to update an Order ?

To modify a specific Order you need to setup it's "id".

Here is an example :

```python
# ORDER SETUP
order = Order(
    id=YOUR_ORDER_ID,
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

To delete a specific Order you just need it's "id".

Here is an example :

```python
# DELETE ORDER
succcess = trading_api.delete_order(order_id=YOUR_ORDER_ID)
```

# 5. Portfolio

## 5.1. How to retrieve pending Orders ?

This is how to get the list of Orders currently created but not yet executed or deleted :
```python
request_list = Update.RequestList()
request_list.values.extend([
    Update.Request(option=Update.Option.ORDERS, last_updated=0),
])

update = trading_api.get_update(request_list=request_list)
update_dict = pb_handler.message_to_dict(message=update)
orders_df = pd.DataFrame(update_dict['orders']['values'])
```

Example : Orders

       product_id      time_type  price  size                                    id  ...  action  order_type stop_price retained_order  sent_to_exchange
    0           0  GOOD_TILL_DAY      2     3  202cb962-ac59-075b-964b-07152d234b70  ...     BUY       LIMIT         16             17                18

For a more comprehensive example :
[update.py](examples/trading/update.py)

## 5.2. How to get the Portfolio ?

This is how to list the stocks/products currently in the portfolio :
```python
request_list = Update.RequestList()
request_list.values.extend([
    Update.Request(option=Update.Option.PORTFOLIO, last_updated=0),
])

update = trading_api.get_update(request_list=request_list)
update_dict = pb_handler.message_to_dict(message=update)
portfolio_df = pd.DataFrame(update_dict['portfolio']['values'])
```

For a more comprehensive example :
[update.py](examples/trading/update.py)

## 5.3. How to get the TotalPortfolio ?

This is how to get aggregated data about the portfolio :
```python
request_list = Update.RequestList()
request_list.values.extend([
    Update.Request(option=Update.Option.TOTALPORTFOLIO, last_updated=0),
])

update = trading_api.get_update(request_list=request_list)
update_dict = pb_handler.message_to_dict(message=update)
total_portfolio_df = pd.DataFrame(update_dict['total_portfolio']['values'])
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
from_date = OrdersHistory.Request.Date(year=2020,month=11,day=15)
to_date = OrdersHistory.Request.Date(year=2020,month=10,day=15)
request = OrdersHistory.Request(from_date=from_date, to_date=to_date)

# FETCH DATA
orders_history = trading_api.get_orders_history(request=request)
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
# SETUP REQUEST
from_date = AccountOverview.Request.Date(year=2020,month=11,day=15)
to_date = AccountOverview.Request.Date(year=2020,month=10,day=15)
request = AccountOverview.Request(from_date=from_date, to_date=to_date)

# FETCH DATA
account_overview = trading_api.get_account_overview(request=request)
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


## 6.5. How to export the table : CashAccountReport ?

It will export a list of cash movements in a specific format.

Available formats :
- CSV
- HTML
- PDF
- XLS

Here is how to get this content in `CSV` format :

```python
# SETUP REQUEST
from_date = CashAccountReport.Request.Date(year=2020,month=11,day=15)
to_date = CashAccountReport.Request.Date(year=2020,month=10,day=15)
request = CashAccountReport.Request(
    format=CashAccountReport.Format.CSV,
    country='FR',
    lang='fr',
    from_date=from_date,
    to_date=to_date,
)

# FETCH DATA
cash_account_report = trading_api.get_cash_account_report(
    request=request,
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

Exact definitions of `CashAccountReport` and `CashAccountReport.Request` are in this file :
[trading.proto](protos/degiro_connector/trading/models/trading.proto)

For a more comprehensive example :
[cash_account_report.py](examples/trading/cash_account_report.py)

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

## 7.2. How to get my favourite products ?

Here is how to get this data :

```python
# FETCH DATA
favourites_list = trading_api.get_favourites_list()
```

For a more comprehensive example :
[favourites_list.py](examples/trading/favourites_list.py)

## 7.3. How to lookup products (search by name) ?

Text research on a financial product.

Here is how to get this data :

```python
# SETUP REQUEST
request = ProductSearch.RequestLookup(
    search_text='APPLE',
    limit=10,
    offset=0,
    product_type_id=1,
)

# FETCH DATA
products_lookup = trading_api.product_search(request=request)
```

For a more comprehensive example :
[product_lookup.py](examples/trading/product_lookup.py)

## 7.4. How to search bonds ?

Here is how to get this data :

```python
# SETUP REQUEST
request = ProductSearch.RequestBonds(
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
bond_list = trading_api.product_search(request=request)
```

For a more comprehensive example :
[product_search.py](examples/trading/product_search.py)

## 7.5. How to search etfs ?

Here is how to get this data :

```python
# SETUP REQUEST
request = ProductSearch.RequestETFs(
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
etf_list = trading_api.product_search(request=request)
```

For a more comprehensive example :
[product_search.py](examples/trading/product_search.py)

## 7.6. How to search funds ?

Here is how to get this data :

```python
# SETUP REQUEST
request = ProductSearch.RequestFunds(
    search_text='',
    offset=0,
    limit=100,
    require_total=True,
    sort_columns='name',
    sort_types='asc',
)

# FETCH DATA
fund_list = trading_api.product_search(request=request)
```

For a more comprehensive example :
[product_search.py](examples/trading/product_search.py)

## 7.7. How to search futures ?

Here is how to get this data :

```python
# SETUP REQUEST
request = ProductSearch.RequestFutures(
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
fund_list = trading_api.product_search(request=request)
```

For a more comprehensive example :
[product_search.py](examples/trading/product_search.py)

## 7.8. How to search leverageds ?

Here is how to get this data :

```python
# SETUP REQUEST
request = ProductSearch.RequestLeverageds(
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
etf_list = trading_api.product_search(request=request)
```

For a more comprehensive example :
[product_search.py](examples/trading/product_search.py)

## 7.9. How to search options ?
Here is how to get this data :

```python
# SETUP REQUEST
request = ProductSearch.RequestOptions(
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
option_list = trading_api.product_search(request=request)
```

For a more comprehensive example :
[product_search.py](examples/trading/product_search.py)

## 7.10. How to search stocks ?

It contains information about available stocks.

Here is how to get this data :

```python
# SETUP REQUEST
request = ProductSearch.RequestStocks(
    index_id=122001,    # NASDAQ 100
    exchange_id=663,    # NASDAQ
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
stock_list = trading_api.product_search(request=request)
```

For a more comprehensive example :
[product_search.py](examples/trading/product_search.py)

## 7.11. How to search warrants ?

Here is how to get this data :

```python
# SETUP REQUEST
request = ProductSearch.RequestWarrants(
    search_text='',
    offset=0,
    limit=100,
    require_total=True,
    sort_columns='name',
    sort_types='asc',
)

# FETCH DATA
warrant_list = trading_api.product_search(request=request)
```

For a more comprehensive example :
[product_search.py](examples/trading/product_search.py)

## 7.12. How to search products from ids ?

Here is how to get this data :

```python
# SETUP REQUEST
request = ProductsInfo.Request()
request.products.extend([96008, 1153605, 5462588])

# FETCH DATA
products_info = trading_api.get_products_info(
    request=request,
    raw=True,
)
```

For a more comprehensive example :
[products_info.py](examples/trading/products_info.py)

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
# SETUP REQUEST
request = Agenda.Request()
request.start_date.FromJsonString('2021-06-21T22:00:00Z')
request.end_date.FromJsonString('2021-11-28T23:00:00Z')
request.calendar_type = Agenda.CalendarType.DIVIDEND_CALENDAR
request.offset = 0
request.limit = 25

# FETCH DATA
agenda = trading_api.get_agenda(
    request=request,
    raw=False,
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

Exact definitions of `Agenda` and `Agenda.Request` are in this file :
[trading.proto](protos/degiro_connector/trading/models/trading.proto)

For a more comprehensive example :
[agenda.py](examples/trading/agenda.py)

# 9. Contributing
Pull requests are welcome.

Feel free to open an issue or send me a message if you have a question.

# 10. License
[BSD-3-Clause License](https://raw.githubusercontent.com/Chavithra/degiro-connector/main/LICENSE)
