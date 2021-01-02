# 1. **Degiro Connector**

This is yet another library to access Degiro's API.

## 1.1. Which features ?
Here are the features you can access through this library :

|**Endpoint**|**Feature(s)**|
|:-|:-|
|AccountOverview|Retrieve all the CashMovements between two dates.|
|Bonds<br>ETFs<br>Funds<br>Futures<br>Leverageds<br>Lookup<br>Options<br>Stocks<br>Warrants|Search list of products according their type and other criterias. <br> For instance all the stocks from NASDAQ 100.|
|ClientDetails|Retrieve a table containing : account information.|
|ClientInfo|Retrieve a table containing : "clientId" and Currencies.|
|Config|Retrieve a table containing : "clientId" and URLs constitutive of Degiro's API.|
|Favourites|Retrieve favorite products lists.|
|Order|Create, update, delete an Order.|
|OrderHistory|Retrieve all Orders created between two dates.|
|Orders|List pending Orders.|
|Portoflio|List products in your Portoflio.|
|ProductLookup|Search a product by it's name.|
|Quotecasts|Fetch real-time data on financial products. <br> For instance the real-time stock Price.|
|TotalPorfolio|Retrieve aggregated information about your assets.|
|TransactionsHistory|Retrieve all Transactions created between two dates.|

## 1.2. How to install ?

```bash
pip install git+https://github.com/chavithra/degiro-connector.git
```

## 1.3. How to uninstall ?

```bash
pip uninstall degiro-connector
```

## 1.4. Table of contents
- [1. **Degiro Connector**](#1-degiro-connector-)
  * [1.1. Which features ?](#11-which-features-)
  * [1.2. How to install ?](#12-how-to-install-)
  * [1.3. How to uninstall ?](#13-how-to-uninstall-)
  * [1.4. Table of contents](#14-table-of-contents)
- [2. Real-time data](#2-real-time-data)
  * [2.1. How to login ?](#21-how-to-login-)
  * [2.2. What is the timeout ?](#22-what-is-the-timeout-)
  * [2.3. How to subscribe to a data-stream ?](#23-how-to-subscribe-to-a-data-stream-)
  * [2.4. How to unsubscribe to a data-stream ?](#24-how-to-unsubscribe-to-a-data-stream-)
  * [2.5. How to fetch the data ?](#25-how-to-fetch-the-data-)
  * [2.6. How to use this data ?](#26-how-to-use-this-data-)
  * [2.7. Which are the available data types ?](#27-which-are-the-available-data-types-)
  * [2.8. What is a Ticker ?](#28-what-is-a-ticker-)
  * [2.9. What is inside the Dictionnary ?](#29-what-is-inside-the-dictionnary-)
  * [2.10. What is inside the DataFrame ?](#210-what-is-inside-the-dataframe-)
- [3. Trading connection](#3-trading-connection)
  * [3.1. What are the credentials ?](#31-what-are-the-credentials-)
  * [3.2. What is the purpose of "in_account" ?](#32-what-is-the-purpose-of-in_account-)
  * [3.3. What is the purpose of "totp_secret_key" ?](#33-what-is-the-purpose-of-totp_secret_key-)
  * [3.4. How to Login ?](#34-how-to-login-)
  * [3.5. How to use 2FA ?](#35-how-to-use-2fa-)
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
  * [6.1. How to retrieve the Config table ?](#61-how-to-retrieve-the-config-table-)
  * [6.2. How to retrieve the ClientDetails table ?](#62-how-to-retrieve-the-clientdetails-table-)
  * [6.3. How to retrieve the ClientInfos table ?](#63-how-to-retrieve-the-clientinfos-table-)
  * [6.4. How to get the AccountOverviews table ?](#64-how-to-get-the-accountoverviews-table-)
- [7. Products](#7-products)
  * [7.1. How to get my favourite products ?](#71-how-to-get-my-favourite-products-)
  * [7.2. How to lookup products (search by name) ?](#72-how-to-lookup-products-search-by-name-)
  * [7.3. How to search bonds ?](#73-how-to-search-bonds-)
  * [7.4. How to search etfs ?](#74-how-to-search-etfs-)
  * [7.5. How to search funds ?](#75-how-to-search-funds-)
  * [7.6. How to search futures ?](#76-how-to-search-futures-)
  * [7.7. How to search leverageds ?](#77-how-to-search-leverageds-)
  * [7.8. How to search options ?](#78-how-to-search-options-)
  * [7.9. How to search stocks ?](#79-how-to-search-stocks-)
  * [7.10. How to search warrants ?](#710-how-to-search-warrants-)
- [8. Contributing](#8-contributing)
- [9. License](#9-license)

# 2. Real-time data

It is possible to fetch a stream of data in real-time from Degiro's API.

For instance if one needs the following data from the "AAPL" stock :
* LastDate
* LastTime
* LastPrice
* LastVolume

He can use this library to retrieve update like this :

    LastDate    LastTime    LastPrice LastVolume
    2020-11-13  22:00:00    119.26    4697040

## 2.1. How to login ?

In order to fetch data you need to establish a connection.

You can use the following code :

```python
# SETUP API
quotecast_api = API(user_token=YOUR_USER_TOKEN) 

# CONNECTION
quotecast_api.connect()
```

Your "user_token" is inside the "config" table.

See section related to "config" table. 

For a more comprehensive example : [realtime_data.py](examples/quotecast/realtime_data.py)

## 2.2. What is the timeout ?

Connection timeout is around 15 seconds.

Which means a connection will cease to work after this timeout.

This timeout is reset each time you use this connection to :
* Subscribe to a metric (for instance a stock Price)
* Fetch the data-stream

So if you use it nonstop (in a loop) you won't need to reconnect.

## 2.3. How to subscribe to a data-stream ?

To subscribe to a data-stream you need to setup a Request message.

A Request has the following parameters :
|**Parameter**|**Type**|**Description**|
|:-|:-|:-|
|subscriptions|google.protobuf.internal.containers.MessageMap|List of products & metrics to subscribe to.|
|unsubscriptions|google.protobuf.internal.containers.MessageMap|List of products & metrics to unsubscribe to.|

Here is an example of request :
```python
request = Request()
request.subscriptions['360015751'].extend([
    'LastPrice',
    'LastVolume',
])
request.subscriptions['AAPL.BATS,E'].extend([
    'LastPrice',
    'LastVolume',
])
```

Once you have built this Request object you can send it to Degiro's API like this :
```python
quotecast_api.subscribe(request=request)
```

For a more comprehensive example : [realtime_data.py](examples/quotecast/realtime_data.py)


## 2.4. How to unsubscribe to a data-stream ?

As for a subscription, to remove metrics from the data-stream you need to setup a Request message.

If you try to unsubscribe to a metric to which you didn't subscribed previously it will most likely have no impact.

A Request has the following parameters :
|**Parameter**|**Type**|**Description**|
|:-|:-|:-|
|subscriptions|google.protobuf.internal.containers.MessageMap|List of products & metrics to subscribe to.|
|unsubscriptions|google.protobuf.internal.containers.MessageMap|List of products & metrics to unsubscribe to.|

Here is an example of request :
```python
request = Request()
request.unsubscriptions['360015751'].extend([
    'LastPrice',
    'LastVolume',
])
request.unsubscriptions['AAPL.BATS,E'].extend([
    'LastPrice',
    'LastVolume',
])
```

Once you have built this Request object you can send it to Degiro's API like this :
```python
quotecast_api.subscribe(request=request)
```

For a more comprehensive example : [realtime_data.py](examples/quotecast/realtime_data.py)

## 2.5. How to fetch the data ?

You can use the following code :
```python
quotecast = quotecast_api.fetch_data()
```

For a more comprehensive example : [realtime_data.py](examples/quotecast/realtime_data.py)

## 2.6. How to use this data ?

Received data is a Quotecast object with the following properties :

|**Parameter**|**Type**|**Description**|
|:-|:-|:-|
|json_data|dict|Dictionnary representation of what Degiro's API has sent.|
|metadata|Metadata|Containing the "response_datetime" and "request_duration".|

Here how to access these properties :
```python
json_data = quotecast.json_data
response_datetime = quotecast.metadata.response_datetime
request_duration= quotecast.metadata.request_duration
```

For a more comprehensive example : [realtime_data.py](examples/quotecast/realtime_data.py)

## 2.7. Which are the available data types ?

This library provides the tools to convert Degiro's JSON data into something more programmer-friendly.

Here is the list of available data type :

|**Type**|**Description**|
|:-|:-|
|Ticker|Protobuf message (for GRPC).|
|Dictionnaries|Standard Python Dictionaries : **dict**.|
|DataFrame|DataFrame from the library Pandas.|

Here is how to build each type :

```python
# BUILD TICKER
quotecast_parser.put_quotecast(quotecast=quotecast)
ticker = quotecast_parser.ticker

# BUILD DICT
ticker_dict = pb_handler.ticker_to_dict(ticker=ticker)

# BUILD PANDAS.DATAFRAME
ticker_df = pb_handler.build_df_from_ticker(ticker=ticker)
```

## 2.8. What is a Ticker ?

The generated Ticker contains :

|**Parameter**|**Type**|**Description**|
|:-|:-|:-|
|metadata|Metadata|Containing the "response_datetime" and "request_duration".|
|products|MessageMap|Dictionnary like object containing the metrics group by "vwd_id".|
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

## 2.9. What is inside the Dictionnary ?

The generated Dictionnary is actually a list of Python Dictionnaries.

Each Dictionnary depicts a product with :
* keys has metrics name.
* values has metrics values

Example - dict :

```python
[
    {
        'vwd_id': 360114899,
        'response_datetime': '2020-11-08 12:00:27',
        'request_duration': 1.0224891666870117,
        'LastDate': '2020-11-06',
        'LastTime': '17:36:17',
        'LastPrice': '70.0',
        'LastVolume': '100'
    },
    {
        'vwd_id': 360015751,
        'response_datetime': '2020-11-08 12:00:27',
        'request_duration': 1.0224891666870117,
        'LastDate': '2020-11-06',
        'LastTime': '17:36:17',
        'LastPrice': '22.99',
        'LastVolume': '470'
    }
]
```
## 2.10. What is inside the DataFrame ?

The generated DataFrame will content :

* In rows : the product, for instance the "AAPL" stock which has "vwd_id" = "AAPL.BATS,E".
* In columns : the product's parameters for instance "LastPrice", "LastVolume",...

Example of DataFrame content :

           vwd_id    response_datetime  request_duration    LastDate  LastTime LastPrice LastVolume
    0   360114899  2020-11-08 12:00:27          1.022489  2020-11-06  17:39:57      70.0        100
    1   360015751  2020-11-08 12:00:27          1.022489  2020-11-06  17:36:17     22.99        470

For a more comprehensive example : [realtime_data.py](examples/quotecast/realtime_data.py)

# 3. Trading connection

This this library contains two connector :
* quotecast.api : to consume real-time data.
* trading.api : to manage your Degiro's Account.

The rest of this document will only refer to "trading.api".

## 3.1. What are the credentials ?

Some credentials are required to use Degiro's trading API.

Here are these credentials :

|**Parameter**|**Type**|**Description**|
|:-|:-|:-|
|username|str|Username used to log into Degiro's website.|
|password|str|Password used to log into Degiro's website.|
|int_account|int|Unique identifier of the account : used by Degiro's server.|
|totp_secret_key|str|Secret key used for Two-factor Authentication (2FA).|

## 3.2. What is the purpose of "in_account" ?

The parameter "int_account" is not necessary for login.

But it is required to do some of the operations available in this connector.

You can get the "int_account" using the "Config" table, it is the parameter "clientId".

## 3.3. What is the purpose of "totp_secret_key" ?

The parameter "totp_secret_key" is only required if you have enabled 2FA on Degiro's website.

When you try to activate 2FA on Degiro's website, it displays some QRCode.

This QRCode changes at each activation.

A QRCode is a picture which can be converted into a text.

You can download this QRCode and use a tool to extract the text from it.

This extracted text will look like this :

    otpauth://totp/DEGIRO:YOUR_USERNAME?algorithm=SHA1&issuer=DEGIRO&secret=YOUR_TOPT_SECRET_KEY&digits=6&period=30

Has you can guess the "totp_secret_key" is in this part :

    secret=YOUR_TOPT_SECRET_KEY

## 3.4. How to Login ?
In order to use the "trading.api" you need to establish a connection.

Here is how to login :
```python
# SETUP CREDENTIALS
credentials = Credentials(
    username = YOUR_USERNAME,
    password = YOUR_PASSWORD,
    int_account = YOUR_INT_ACCOUNT, # OPTIONAL FOR LOGIN
)

# SETUP TRADING API
trading_api = API(credentials=credentials)

# ESTABLISH CONNECTION
trading_api.connect()
```

## 3.5. How to use 2FA ?
If you are using Two-factor Authentication (2FA) you need to provide an extra parameter.

This parameter is called "totp_secret_key" by the library.

See the section about "totp_secret_key" to know how to get this parameter from Degiro's website.

```python
# SETUP CREDENTIALS
credentials = Credentials(
    username = YOUR_USERNAME,
    password = YOUR_PASSWORD,
    int_account = YOUR_INT_ACCOUNT, # OPTIONAL FOR LOGIN
    totp_secret_key = YOUR_2FA_SECRET_KEY, # ONLY IF 2FA IS ENABLED
)

# SETUP TRADING API
trading_api = API(credentials=credentials)

# ESTABLISH CONNECTION
trading_api.connect()
```

# 4. Order

Here are the main parameters of an Order.

|**Parameter**|**Type**|**Description**|
|:-|:-|:-|
|action|Order.Action|Whether you want to : BUY or SELL.|
|order_type|Order.OrderType|Type of order : LIMIT, STOP_LIMIT, MARKET or STOP_LOSS.|
|price|float|Price of the order.|
|product_id|int|Identifier of the product concerned by the order.|
|size|float|Size of the order.|
|time_type|Order.TimeType|Duration of the order : GOOD_TILL_DAY or GOOD_TILL_CANCELED|

The full description of an Order is available here : [trading.proto](protos/trading/pb/trading.proto)

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
|response_datetime|str|ISO format datetime of the checking operation.|
|transaction_fees|repeated google.protobuf.Struct|Transaction fees that will be applied to the Order.|
|transaction_opposite_fees|repeated google.protobuf.Struct|Other kind of fees that will be applied to the Order.|
|transaction_taxes|repeated google.protobuf.Struct|Taxes that will be applied to the Order.|

Here are the parameters of a ConfirmationResponse :

|**Parameter**|**Type**|**Description**|
|:-|:-|:-|
|orderId|str|Id of the created Order.|
|response_datetime|str|ISO format datetime of the confirmation operation.|

Here is an example :

```python
# ORDER SETUP
order = Order(
    action = Order.Action.BUY,
    order_type = Order.OrderType.LIMIT,
    price = 10,
    product_id = 71981,
    size = 1,
    time_type = Order.TimeType.GOOD_TILL_DAY,
)

# FETCH CONFIRMATION_ID
checking_response = trading_apicheck_order(order=order)

# SEND CONFIRMATION
confirmation_response = trading_api.confirm_order(
    confirmation_id = confirmation_id,
    order = order
)
```

## 4.2. How to update an Order ?

To modify a specific Order you need to setup it's "id".

Here is an example :

```python
# ORDER SETUP
order = Order(
    id = YOUR_ORDER_ID
    action = Order.Action.BUY,
    order_type = Order.OrderType.LIMIT,
    price = 10.60,
    product_id = 71981,
    size = 1,
    time_type = Order.TimeType.GOOD_TILL_DAY,
)

# UPDATE ORDER
succcess = trading_api.update_order(order=order)
```

## 4.3. How to delete an Order ?

To delete a specific Order you just need it's "id".

Here is an example :

```python
# DELETE ORDER
succcess = trading_api.delete(order_id=YOUR_ORDER_ID)
```

# 5. Portfolio

## 5.1. How to retrieve pending Orders ?

This is how to get the list of Orders currently created but not yet executed or deleted :
```python
request_list = Update.RequestList()
request_list.values.extend(
    [
        Update.Request(
            option = Update.Option.ORDERS,
            last_updated = 0,
        ),
    ]
)

update = trading_api.get_update(request_list=request_list)
update_dict = pb_handler.message_to_dict(message=update)
orders_df = pd.DataFrame(update_dict['orders']['values'])
```

Example : Orders

       product_id      time_type  price  size                                    id  ...  action  order_type stop_price retained_order  sent_to_exchange
    0           0  GOOD_TILL_DAY      2     3  202cb962-ac59-075b-964b-07152d234b70  ...     BUY       LIMIT         16             17                18

For a more comprehensive example : [update.py](examples/trading/update.py)

## 5.2. How to get the Portfolio ?

This is how to list the stocks/products currently in the portfolio :
```python
request_list = Update.RequestList()
request_list.values.extend(
    [
        Update.Request(
            option = Update.Option.PORTFOLIO,
            last_updated = 0,
        ),
    ]
)

update = trading_api.get_update(request_list=request_list)
update_dict = pb_handler.message_to_dict(message=update)
portfolio_df = pd.DataFrame(update_dict['portfolio']['values'])
```

For a more comprehensive example : [update.py](examples/trading/update.py)

## 5.3. How to get the TotalPortfolio ?

This is how to get aggregated data about the portfolio :
```python
request_list = Update.RequestList()
request_list.values.extend(
    [
        Update.Request(
            option = Update.Option.TOTALPORTFOLIO,
            last_updated = 0,
        ),
    ]
)

update = trading_api.get_update(request_list=request_list)
update_dict = pb_handler.message_to_dict(message=update)
total_portfolio_df = pd.DataFrame(update_dict['total_portfolio']['values'])
```

Example : DataFrame

       degiroCash  flatexCash  totalCash  totalDepositWithdrawal  todayDepositWithdrawal  ...  reportNetliq  reportOverallMargin  reportTotalLongVal  reportDeficit  marginCallStatus
    0           0           1          2                       3                       4  ...            16                   17                  18             19    NO_MARGIN_CALL

For a more comprehensive example : [update.py](examples/trading/update.py)


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
# PREPARE REQUEST
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
# PREPARE REQUEST
from_date = TransactionsHistory.Request.Date(year=2020,month=11,day=15)
to_date = TransactionsHistory.Request.Date(year=2020,month=10,day=15)
request = TransactionsHistory.Request(from_date=from_date, to_date=to_date)

# FETCH DATA
transactions_history = trading_api.get_transactions_history(request=request)
```

For a more comprehensive example :
[transactions_history.py](examples/trading/transactions_history.py)

# 6. Account

## 6.1. How to retrieve the Config table ?

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
config_table = trading_api.get_config()
```

For a more comprehensive example : [config_table.py](examples/trading/config_table.py)

## 6.2. How to retrieve the ClientDetails table ?

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
client_details_table = trading_api.get_client_details()
```

For a more comprehensive example :
[client_details_table.py](examples/trading/client_details_table.py)

## 6.3. How to retrieve the ClientInfos table ?

The ClientInfos table contains the following information about currencies.

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

## 6.4. How to get the AccountOverviews table ?

It contains information about cash movements.

Here is how to get this data :

```python
# PREPARE REQUEST
from_date = AccountOverview.Request.Date(year=2020,month=11,day=15)
to_date = AccountOverview.Request.Date(year=2020,month=10,day=15)
request = AccountOverview.Request(from_date=from_date, to_date=to_date)

# FETCH DATA
account_overview = trading_api.get_account_overview(request=request)
```

For a more comprehensive example : [account_overview.py](examples/trading/account_overview.py)

# 7. Products

## 7.1. How to get my favourite products ?

Here is how to get this data :

```python
# FETCH DATA
favourites_list = trading_api.get_favourites_list()
```

For a more comprehensive example : [favourites_list.py](examples/trading/favourites_list.py)

## 7.2. How to lookup products (search by name) ?

Text research on a financial product.

Here is how to get this data :

```python
# PREPARE REQUEST
request = ProductSearch.RequestLookup(
    search_text = 'APPLE',
    limit = 10,
    offset = 0,
)

# FETCH DATA
products_lookup = trading_api.product_search(request=request)
```

For a more comprehensive example : [products_lookup.py](examples/trading/products_lookup.py)

## 7.3. How to search bonds ?

Here is how to get this data :

```python
# PREPARE REQUEST
request = ProductSearch.RequestBonds(
    bondIssuerTypeId=0,
    bondExchangeId=710,

    searchText='',
    offset=0,
    limit=100,
    requireTotal=True,
    sortColumns='name',
    sortTypes='asc',
)

# FETCH DATA
bond_list = trading_api.product_search(request=request)
```

For a more comprehensive example : [product_search.py](examples/trading/product_search.py)


## 7.4. How to search etfs ?

Here is how to get this data :

```python
# PREPARE REQUEST
request = ProductSearch.RequestETFs(
    popularOnly=False,
    inputAggregateTypes='',
    inputAggregateValues='',

    searchText='',
    offset=0,
    limit=100,
    requireTotal=True,
    sortColumns='name',
    sortTypes='asc',
)

# FETCH DATA
etf_list = trading_api.product_search(request=request)
```

For a more comprehensive example : [product_search.py](examples/trading/product_search.py)

## 7.5. How to search funds ?

Here is how to get this data :

```python
# PREPARE REQUEST
request = ProductSearch.RequestFunds(
    searchText='',
    offset=0,
    limit=100,
    requireTotal=True,
    sortColumns='name',
    sortTypes='asc',
)

# FETCH DATA
fund_list = trading_api.product_search(request=request)
```

For a more comprehensive example : [product_search.py](examples/trading/product_search.py)

## 7.6. How to search futures ?

Here is how to get this data :

```python
# PREPARE REQUEST
request = ProductSearch.RequestFutures(
    futureExchangeId=1,
    underlyingIsin='FR0003500008',

    searchText='',
    offset=0,
    limit=100,
    requireTotal=True,
    sortColumns='name',
    sortTypes='asc',
)

# FETCH DATA
fund_list = trading_api.product_search(request=request)
```

For a more comprehensive example : [product_search.py](examples/trading/product_search.py)

## 7.7. How to search leverageds ?

Here is how to get this data :

```python
# PREPARE REQUEST
request = ProductSearch.RequestLeverageds(
    popularOnly=False,
    inputAggregateTypes='',
    inputAggregateValues='',

    searchText='',
    offset=0,
    limit=100,
    requireTotal=True,
    sortColumns='name',
    sortTypes='asc',
)

# FETCH DATA
etf_list = trading_api.product_search(request=request)
```

For a more comprehensive example : [product_search.py](examples/trading/product_search.py)

## 7.8. How to search options ?
Here is how to get this data :

```python
# PREPARE REQUEST
request = ProductSearch.RequestOptions(
    inputAggregateTypes='',
    inputAggregateValues='',
    optionExchangeId=3,
    underlyingIsin='FR0003500008',

    searchText='',
    offset=0,
    limit=100,
    requireTotal=True,
    sortColumns='name',
    sortTypes='asc',
)

# FETCH DATA
option_list = trading_api.product_search(request=request)
```

For a more comprehensive example : [product_search.py](examples/trading/product_search.py)

## 7.9. How to search stocks ?

It contains information about available stocks.

Here is how to get this data :

```python
# PREPARE REQUEST
request = ProductSearch.RequestStocks(
    indexId=5,
    isInUSGreenList=False,
    stockCountryId=886,

    searchText='',
    offset=0,
    limit=100,
    requireTotal=True,
    sortColumns='name',
    sortTypes='asc',
)

# FETCH DATA
stock_list = trading_api.product_search(request=request)
```

For a more comprehensive example : [product_search.py](examples/trading/product_search.py)

## 7.10. How to search warrants ?

Here is how to get this data :

```python
# PREPARE REQUEST
request = ProductSearch.RequestWarrants(
    searchText='',
    offset=0,
    limit=100,
    requireTotal=True,
    sortColumns='name',
    sortTypes='asc',
)

# FETCH DATA
warrant_list = trading_api.product_search(request=request)
```

For a more comprehensive example : [product_search.py](examples/trading/product_search.py)

# 8. Contributing
Pull requests are welcome.

Feel free to open an issue or send me a message if you have a question.

# 9. License
[BSD-3-Clause License](https://raw.githubusercontent.com/Chavithra/degiro_connector/master/LICENSE)
