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
    vwd_id=360015751,
    label_list=[
        'LastDate',
        'LastTime',
        'LastPrice',
        'LastVolume',
        'OpenPrice',
        'HighPrice',
        'LowPrice',
        'ClosePrice',
        'PreviousClosePrice',
    ],
)
api.subscribe(request=request)
# FETCH DATA
while True:
    data = api.fetch_data()
```

For a more comprehensive example : examples.quotecast.realtimedata

## 2. Order

### 2. Order - Create
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

### 2. Order - Update

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

### Delete an Order

```python
status = api.delete(order_id=YOUR_ORDER_ID)
```

# Contributing
Pull requests are welcome.

Feel free to open an issue or send me a message if you have a question.

# License
[BSD-3-Clause License](https://raw.githubusercontent.com/Chavithra/degiro_connector/master/LICENSE)

# Note
* A minor issue :
    In the payload from the following URL :
        https://trader.degiro.nl/trading/secure/v5/update
    In the attribute "orders" of this payload.
    Inside an Order :
        - "date" field is the "hour of the day" when it's a Sell Order.
        - "date" field is the "date of the day" when it's a Buy Order.
