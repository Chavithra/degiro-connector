# **Degiro Connector**

## Features
This library will allow you to connect to Degiro's website and to use :
1. **Realtime data** (last price, volume, high, low, open, close,...)
2. **Order** (creation/update/delete)
3. **Portfolio** (alerts, cash funds, orders, transactions)
4. **TotalPortfolio** (free space, porfolio value, total cash,...)
5. **OrderHistory**
6. **TransactionsHistory**
7. **ClientInfo**
8. **ClientDetails**
9. **AccountOverview** (cashMovements)
10. **ProductLookup**

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

## **Examples**

## 1. Realtime data

```python
# SETUP API
api = API(user_token=YOUR_TOKEN)
# CONNECTION
api.connection_storage.connect()
# SUBSCRIBE TO FEED
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
quotecast = api.fetch_data()

# DISPLAY RAW JSON
print(quotecast.json_data)

# DISPLAY TICKER (PROTOBUF/GRPC OBJECT)
quotecast_parser.put_quotecast(quotecast=quotecast)
ticker = quotecast_parser.ticker

# DISPLAY DICT
record_list = pb_handler.build_dict_from_ticker(ticker=ticker)
print(record_list)

# DISPLAY PANDAS.DATAFRAME
df = pb_handler.build_df_from_ticker(ticker=ticker)
print(df)
```

Example - DISPLAY PANDAS.DATAFRAME :

       product_id    response_datetime  request_duration    LastDate  LastTime LastPrice LastVolume
    0   360114899  2020-11-08 02:40:27          1.022489  2020-11-06  17:39:57      70.0        100
    1   360015751  2020-11-08 02:40:27          1.022489  2020-11-06  17:36:17     22.99        470

For a more comprehensive example : [realtime_data.py](examples/quotecast/realtime_data.py)

## 2. Order

### 2.1 Order - Create
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

### 2.2 Order - Update

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

### 2.2 Order - Delete

```python
status = api.delete(order_id=YOUR_ORDER_ID)
```

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
