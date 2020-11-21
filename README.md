# **Degiro Connector**

This is yet another library to access Degiro's API.

## Which features ?
This library will allow you to access the following features from
Degiro's API :

|**Feature**|**Description**|
|:-|:-|
|Real-time data|Fetch financial product's properties.<br> For instance the real-time stock Price/Volume.|
|Order|Create, update, delete an Order.|
|Orders|Check the state of pending Orders.|
|Portoflio|Check the state of bought financial products (share/etf...).|
|TotalPorfolio|Have aggregated information about your assets.|
|OrderHistory|Information about all Orders created between two dates.|
|TransactionsHistory|Information about the Transactions created between two dates.|
|ClientInfo|Client id and information about currencies.|
|ClientDetails|Information about the Account.|
|AccountOverview|Information about the CashMovements between two dates.|
|ProductLookup|To search information about a specific financial product.|
|Config|Table with "clientId" and URLs constitutive of Degiro's API.|

## How to install ?

```bash
pip install git+https://github.com/chavithra/degiro-connector.git
```

## How to uninstall ?

```bash
pip uninstall degiro-connector
```

# 1. Real-time data

It is possible to fetch a stream of data in real-time from Degiro's API.

For instance if one needs the following data from the "AAPL" stock :
* LastDate
* LastTime
* LastPrice
* LastVolume

He can use this library to retrieve update like this :

    LastDate    LastTime    LastPrice LastVolume
    2020-11-13  22:00:00    119.26    4697040

## 1.1. How to login ?

In order to fetch data you need to establish a connection.

You can use the following code :

```python
# SETUP API
quotecast_api = API(user_token=YOUR_USER_TOKEN) 

# CONNECTION
quotecast_api.connection_storage.connect()
```

Your "user_token" is inside the "config" table.

See section related to "config" table. 

For a more comprehensive example : [realtime_data.py](examples/quotecast/realtime_data.py)

## 1.2. What is the timout ?

Connection timeout is around 15 seconds.

Which means a connection will cease to work after this timeout.

This timeout is reset each time you use this connection to :
* Subscribe to a data-stream
* Fetch the data-stream

So if you use it nonstop (in a loop) you won't need to reconnect.

## 1.3. How to subscribe to a data-stream ?

To subscribe to a data-stream you need to setup a Request.

A Request has the following parameters :

|**Parameter**|**Type**|**Description**|
|:-|:-|:-|
|action|Request.Action|SUBSCRIBE / UNSUBSCRIBE|
|vwd_id|str|Identifier of the product.|
|label_list|List[str]|List of data you want to retrieve.|

You can use the following code :
```python
request = Request(
    action = Request.Action.SUBSCRIBE,
    vwd_id = '360015751',
    label_list = ['LastDate','LastTime','LastPrice','LastVolume'],
)
```

Once you have built this Request object you can send it to Degiro's API like this :
```python
quotecast_api.subscribe(request=request)
```

For a more comprehensive example : [realtime_data.py](examples/quotecast/realtime_data.py)

## 1.4. How to fetch the data ?

You can use the following code :
```python
quotecast = quotecast_api.fetch_data()
```

For a more comprehensive example : [realtime_data.py](examples/quotecast/realtime_data.py)

## 1.5. How can I use this data ?

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

## 1.6. Which data type ?

This library provides the tools to convert Degiro's JSON data into
something more programmer-friendly.

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
ticker_dict = pb_handler.build_dict_from_ticker(ticker=ticker)

# BUILD PANDAS.DATAFRAME
ticker_df = pb_handler.build_df_from_ticker(ticker=ticker)
```

## 1.7. What is a Ticker ?

The generated Ticker contains :

|**Parameter**|**Type**|**Description**|
|:-|:-|:-|
|metadata|Metadata|Containing the "response_datetime" and "request_duration".|
|products|MessageMap|Dictionnary like object containing the metrics group by "product_id".|
|product_list|RepeatedScalarFieldContainer|List of available "product_id".|

Here are some operations available :

```python
product_id = 331868
metric_name = 'LastPrice'

# ACCESS SPECIFIC PRODUCT
product = ticker.products[product_id]

# ACCESS SPECIFIC METRIC
metric = product[metric_name]

# LOOP OVER PRODUCTS
for product_id in ticker.products:
    product = ticker.products[product_id]

# LOOP OVER METRICS
for metric_name in product.metrics:
    metric = product.metrics[metric_name]
```

A Ticker is a custom Protocol Buffer Message built for this library.

It can be transmitted over GRPC framework.

## 1.8. What is inside the Dictionnary ?

The generated Dictionnary is actually a list of Python Dictionnaries.

Each Dictionnary depicts a product with :
* keys has metrics name.
* values has metrics values

Example - dict :

```python
[
    {
        'product_id': 360114899,
        'response_datetime': '2020-11-08 12:00:27',
        'request_duration': 1.0224891666870117,
        'LastDate': '2020-11-06',
        'LastTime': '17:36:17',
        'LastPrice': '70.0',
        'LastVolume': '100'
    },
    {
        'product_id': 360015751,
        'response_datetime': '2020-11-08 12:00:27',
        'request_duration': 1.0224891666870117,
        'LastDate': '2020-11-06',
        'LastTime': '17:36:17',
        'LastPrice': '22.99',
        'LastVolume': '470'
    }
]
```
## 1.9. What is inside the DataFrame ?

The generated DataFrame will content :

* In row : the product, for instance the "AAPL" stock which has "product_id = 331868".
* In columns : the product's parameters for instance "LastPrice", "LastVolume",...

Example of DataFrame content :

       product_id    response_datetime  request_duration    LastDate  LastTime LastPrice LastVolume
    0   360114899  2020-11-08 12:00:27          1.022489  2020-11-06  17:39:57      70.0        100
    1   360015751  2020-11-08 12:00:27          1.022489  2020-11-06  17:36:17     22.99        470

For a more comprehensive example : [realtime_data.py](examples/quotecast/realtime_data.py)

# 2. Trading

This this library contains two connector :
* quotecast.api : to consume real-time data
* trading.api : to manage your Degiro's Account

The rest of this document will only refers to "trading.api".

## 2.1. How to Login ?
In order to use the "trading.api" you need to establish a connection.

Here is how to login :
```python
# SETUP CREDENTIALS
credentials = Credentials(
    int_account = YOUR_INT_ACCOUNT, # OPTIONAL FOR LOGIN
                                    # BUT USED FOR SOME OPERATIONS
    username = YOUR_USERNAME,
    password = YOUR_PASSWORD,
)

# SETUP TRADING API
trading_api = API(credentials=credentials)

# ESTABLISH CONNECTION
trading_api.connection_storage.connect()
```

The "int_account" is not necessary to login.

But it is required to do some of the operations available in this connector.

## 2.1. How to get the credentials ?

Here are the credentials required :
* username : the one you use to login on Degiro's website.
* password : the one you use to login on Degiro's website.
* int_account : it's the "clientId" parameter you can retrieve from "config" table.

The "config" table is described in the section : "5. Config Table".

# 3. Order

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

## 3.1. Order - Create

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

## 3.2. Order - Update

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

## 3.3. Order - Delete

To delete a specific Order you just need it's "id".

Here is an example :

```python
# DELETE ORDER
succcess = trading_api.delete(order_id=YOUR_ORDER_ID)
```

# 4. Orders

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
update_dict = pb_handler.build_dict_from_message(message=update)
orders_df = pd.DataFrame(update_dict['orders']['values'])
```

Example : Orders

       product_id      time_type  price  size                                    id  ...  action  order_type stop_price retained_order  sent_to_exchange
    0           0  GOOD_TILL_DAY      2     3  202cb962-ac59-075b-964b-07152d234b70  ...     BUY       LIMIT         16             17                18

For a more comprehensive example : [update.py](examples/trading/update.py)

# 5. TotalPortfolio

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
update_dict = pb_handler.build_dict_from_message(message=update)
total_portfolio_df = pd.DataFrame(update_dict['total_portfolio']['values'])
```

Example : DataFrame

       degiroCash  flatexCash  totalCash  totalDepositWithdrawal  todayDepositWithdrawal  ...  reportNetliq  reportOverallMargin  reportTotalLongVal  reportDeficit  marginCallStatus
    0           0           1          2                       3                       4  ...            16                   17                  18             19    NO_MARGIN_CALL

For a more comprehensive example : [update.py](examples/trading/update.py)

# 6. Config Table

The config table contains the following informations :

|**Parameter**|**Type**|**Description**|
|:-|:-|:-|
|sessionId|str|Current session id.|
|clientId|int|Unique Degiro's Account identifier also called "intAccount"|
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

# 7. ClientDetails Table

The ClientDetails table contains information about the current Degiro Account.

Example of empty ClientDetails :
```python
{
    'data': {
        'id': int(),
        'intAccount': int(),
        'loggedInPersonId': int(),
        'clientRole': str(),
        'effectiveClientRole': str(),
        'contractType': str(),
        'username': str(),
        'displayName': str(),
        'email': str(),
        'firstContact': {
            'firstName': str(),
            'lastName': str(),
            'displayName': str(),
            'nationality': str(),
            'gender': str(),
            'dateOfBirth': str(),
            'placeOfBirth': str(),
            'countryOfBirth': str()
        },
        'address': {
            'streetAddress': str(),
            'streetAddressNumber': str(),
            'zip': str(),
            'city': str(),
            'country': str()
        },
        'cellphoneNumber': str(),
        'locale': str(),
        'language': str(),
        'culture': str(),
        'bankAccount': {
            'bankAccountId': int(),
            'bic': str(),
            'iban': str(),
            'status': str()
        },
        'flatexBankAccount': {
            'bic': str(),
            'iban': str()
        },
        'memberCode': str(),
        'isWithdrawalAvailable': bool(),
        'isAllocationAvailable': bool(),
        'isIskClient': bool(),
        'isCollectivePortfolio': bool(),
        'isAmClientActive': bool(),
        'canUpgrade': bool()
    }
}
```

Here is how to get this table :

```python
client_details_table = trading_api.get_client_details()
```

For a more comprehensive example : [client_details_table.py](examples/trading/client_details_table.py)

# 8. ClientInfos Table

The ClientInfos table contains information about currencies.

Example of empty ClientInfos :
```python
{
    'data': {
        'clientId': int(),
        'baseCurrency': str(),
        'currencyPairs': {
            'HRKEUR': {
                'id': -1,
                'price': str()
            },
            'USDRUB': {
                'id': 1331862,
                'price': str()
            },
            ...
        },
        'marginType': str(),
        'cashFunds': {
            'CHF': [
                {
                    'id': 210,
                    'name': str(),
                    'productIds': [
                        4667925
                    ]
                }
            ],
            'EUR': [
                {
                    'id': 2432,
                    'name': str(),
                    'productIds': [
                        17707507
                    ]
                }
            ],
            ...
        },
        'compensationCapping': float()
    }
}
```

Here is how to get this table :

```python
client_info_table = trading_api.get_client_info()
```

For a more comprehensive example : [client_info_table.py](examples/trading/client_info_table.py)

# Contributing
Pull requests are welcome.

Feel free to open an issue or send me a message if you have a question.

# License
[BSD-3-Clause License](https://raw.githubusercontent.com/Chavithra/degiro_connector/master/LICENSE)
