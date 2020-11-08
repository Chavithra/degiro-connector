# **Degiro Connector**

## Features
This library will allow you to connect to Degiro's website and to use :
1. **Realtime data** (last price, volume, high, low, open, close,...)
2. **Order** (creation/update/delete)
3. **Orders**
4. **Portfolio** (alerts, cash funds, orders, transactions)
5. **TotalPortfolio** (free space, porfolio value, total cash,...)
6. **OrderHistory**
7. **TransactionsHistory**
8. **ClientInfo**
9. **ClientDetails**
10. **AccountOverview** (cashMovements)
11. **ProductLookup**

## Install
You can install it directly from Github, using the command :

```bash
pip install git+https://github.com/chavithra/degiro-connector.git
```

## Uninstall
Here is the command to remove it from your system :
```bash
pip uninstall degiro-connector
```

## 1. Realtime data


### 1.1. Realtime data - Quotecast

```python
# SUBSCRIBE TO A FEED
request = Request(
    action=Request.Action.SUBSCRIBE,
    vwd_id='360015751',
    label_list=[
        'LastDate',
        'LastTime',
        'LastPrice',
        'LastVolume',
    ],
)
api.subscribe(request=request)

# FETCH DATA
quotecast = api.fetch_data()
```

For a more comprehensive example : [realtime_data.py](examples/quotecast/realtime_data.py)

### 1.2. Realtime data - Raw JSON

```python
# RAW JSON
quotecast.json_data
```

For a more comprehensive example : [realtime_data.py](examples/quotecast/realtime_data.py)

### 1.3. Realtime data - Ticker / Dictionnaries / DataFrame

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
    action=Action.Value('BUY'),
    order_type=OrderType.Value('LIMIT'),
    price=10,
    product_id=71981,
    size=1,
    time_type=TimeType.Value('GOOD_TILL_DAY')
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
    action=Action.Value('BUY'),
    order_type=OrderType.Value('LIMIT'),
    price=10.60,
    product_id=71981,
    size=1,
    time_type=TimeType.Value('GOOD_TILL_DAY')
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
            last_update=0,
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
            last_update=0,
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

# Note
**A minor issue in Degiro's API** :

    In the payload from the following URL :
    https://trader.degiro.nl/trading/secure/v5/update
    In the attribute "orders" of this payload.
    Inside an Order :
        * "date" field is the "hour of the day" when it's a Sell Order.
        * "date" field is the "date of the day" when it's a Buy Order.

# Contributing
Pull requests are welcome.

Feel free to open an issue or send me a message if you have a question.

# License
[BSD-3-Clause License](https://raw.githubusercontent.com/Chavithra/degiro_connector/master/LICENSE)
