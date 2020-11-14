# **Degiro Connector**

This is yet another library to access Degiro's API.
## Which features ?
This library will allow you to access the following features from
Degiro's API :

|Feature|Description|
|:-|:-|
|Real-time data|Fetch financial product's properties.<br> For instance the real-time stock Price/Volume.|
|Order|Create, update, delete an ORDER.|
|Orders|Check the state of pending orders.|
|Portoflio|Check the state of bought financial products (share/etf...)|
|TotalPorfolio|Have aggregated information about your assets|
|OrderHistory||
|TransactionsHistory||
|ClientInfo||
|ClientDetails||
|AccountOverview||
|ProductLookup|To search information about a specific financial product.|
|Config|Table with "clientId" and URLs constitutive of Degiro's API |

## How to install ?

```bash
pip install git+https://github.com/chavithra/degiro-connector.git
```

## How to uninstall
```bash
pip uninstall degiro-connector
```

# 1. Real-time data

It is possible to fetch a stream of data in real-time from Degiro's API.

For instance if one needs the following data from the "APPL" stock :
* LastDate
* LastTime
* LastPrice
* LastVolume

He can use this library to retrieve update like this :

    LastDate    LastTime    LastPrice LastVolume
    2020-11-13  22:00:00    119.26    4697040

## 1.2 How to login ?

In order to fetch data you need to establish a connection.

You can use the following code :

```python
# SETUP API
quotecast_api = QuotecastAPI(user_token=YOUR_USER_TOKEN) 

# CONNECTION
quotecast_api.connection_storage.connect()
```

Your "user_token" is inside the "config" table.

See section related to "config" table. 

## 1.3 What is the timout ?
Connection timeout is around 15 seconds.

Which means a connection will cease to work after this timeout.

This timeout is reset each time you use this connection to :
* Subscribe to a data-stream
* Fetch the data-stream

So if you use it nonstop (in a loop) you won't need to reconnect.

## 1.4. How to subscribe to a data-stream ?
To subscribe to a data-stream you need to setup a Request.

A Request has the following parameters :

|Parameter|Type|Description|
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

Once you built this Request object you can send it to Degiro's API.

You can use the following code :
```python
api.subscribe(request=request)
```


## 1.5. How to fetch the data ?

You can use the following code :
```python
quotecast = api.fetch_data()
```

## 1.6. How can I use this data ?

Received data is a Quotecast object with the following properties :

|Parameter|Type|Description|
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

## 1.6. Data conversion (Ticker / Dict / DataFrame)

This **quotecast** can be converted into :
|Type|Description|
|:-|:-|
|**Ticker**|Protobuf message (for GRPC)|
|**Dictionnaries**|Standard Python Dictionaries : **dict**|
|**DataFrame**|DataFrame from the library Pandas|

```python
# BUILD TICKER (PROTOBUF/GRPC OBJECT)
quotecast_parser.put_quotecast(quotecast=quotecast)
ticker = quotecast_parser.ticker

# BUILD DICT
ticker_dict = pb_handler.build_dict_from_ticker(ticker=ticker)

# BUILD PANDAS.DATAFRAME
ticker_df = pb_handler.build_df_from_ticker(ticker=ticker)
```

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

Example - DataFrame :

       product_id    response_datetime  request_duration    LastDate  LastTime LastPrice LastVolume
    0   360114899  2020-11-08 12:00:27          1.022489  2020-11-06  17:39:57      70.0        100
    1   360015751  2020-11-08 12:00:27          1.022489  2020-11-06  17:36:17     22.99        470

For a more comprehensive example : [realtime_data.py](examples/quotecast/realtime_data.py)

## 2. Order

### 2.1. Order - Create
```python
# ORDER SETUP
order = Order(
    action=Order.Action.BUY,
    order_type=Order.OrderType.LIMIT,
    price=10,
    product_id=71981,
    size=1,
    time_type=Order.TimeType.GOOD_TILL_DAY,
)

# FETCH CONFIRMATION_ID
confirmation_id = api.check_order(order=order)

# SEND CONFIRMATION
order = api.confirm_order(
    confirmation_id=confirmation_id,
    order=order
)
```

### 2.2. Order - Update

```python
# ORDER SETUP
order = Order(
    id=YOUR_ORDER_ID
    action=Order.Action.BUY,
    order_type=Order.OrderType.LIMIT,
    price=10.60,
    product_id=71981,
    size=1,
    time_type=Order.TimeType.GOOD_TILL_DAY,
)

# UPDATE ORDER
status_code = api.update_order(order=order)
```

### 2.2. Order - Delete

```python
status = api.delete(order_id=YOUR_ORDER_ID)
```
### 3. Orders

```python
request_list = Update.RequestList()
request_list.values.extend(
    [
        Update.Request(
            option=Update.Option.ORDERS,
            last_updated=0,
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

For a more comprehensive example : [update.py](examples/quotecast/update.py)

### 5. TotalPortfolio

```python
request_list = Update.RequestList()
request_list.values.extend(
    [
        Update.Request(
            option=Update.Option.TOTALPORTFOLIO,
            last_updated=0,
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

For a more comprehensive example : [update.py](examples/quotecast/update.py)

# Contributing
Pull requests are welcome.

Feel free to open an issue or send me a message if you have a question.

# License
[BSD-3-Clause License](https://raw.githubusercontent.com/Chavithra/degiro_connector/master/LICENSE)
