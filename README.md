# Degiro Connector

Yet another library to handle Degiro's API.

## Features

* [Create/Confirm an Order](#createconfirm-an-order)
* [Update an Order](#update-an-order)
* [Delete an Order](#delete-an-order)
* [Collect financial data](#data-collection)

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
## Create/Confirm an Order
To work with Orders you need to use the class : **trading.api**.

You can use this code :

```python
# ORDER SETUP
order = Order(
    action=Action.Value('BUY'),
    order_type=OrderType.Value('LIMIT'),
    price=10.60,
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

## Update an Order
To work with Orders you need to use the class : **trading.api**.

You can use this code :

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

## Delete an Order
To work with Orders you need to use the class : **trading.api**

You can use this code :

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

# DELETE ORDER
status = api.delete(order_id=order.id)

# OTHER SOLUTION
status = api.delete(order_id=YOUR_ORDER_ID)
```

## Data collection
To fetch Quotecasts you need to use the class : **quotecast.api**

You can use this code :

```python
# REQUEST SETUP
subscription_request = SubscriptionRequest(
    action=Action.SUBSCRIBE,
    product_id=360015751,
    label_list=[
        'LastDate',
        'LastTime',
        'LastPrice',
        'LastVolume',
    ],
)

# SEND REQUEST
api.subscribe(subscription_request=subscription_request)

# FETCH DATA
while True:
    raw_response = api.fetch_data()
    print(raw_response)
```

For a more comprehensive example : [quotecast.applications.fetch_data](quotecast/applications/commands/fetch_data.py)


## Connection

### Why a connection ?

Most of Degiro's API features require a **session**.

There are two kinds of **session**:
 1. **quotecast_session** : to collect financial data
 2. **trading_session** : to do trading operations

### What is the **session** duration ?
The connection has a timeout after which it will cease to work.  
Same thing if you disconnect (using the right API call).

According to my test, it is safe to assume these durations :
 1. **quotecast_session** : at least 15 seconds
 2. **trading_session** : at least 30 minutes

### How connect for Trading ?
You can use this code :
```python
#!/usr/bin/env python3
from trading.api import API
from trading.pb.trading_pb2 import Credentials

# USER_TOKEN SETUP
int_account = YOUR_INT_ACCOUNT
username = YOUR_USERNAME
password = YOUR_PASSWORD

# API SETUP
credentials = Credentials(
    int_account=int_account,
    username=username,
    password=password
)
api = API(credentials=credentials)

# CONNECTION
api.connection_storage.connect()

# DISPLAY SESSION_ID
session_id = api.connection_storage.session_id

print(session_id)
```

### How connect for Quotecasts ?
You can use this code :
```python
#!/usr/bin/env python3
from quotecast.api import API
from quotecast.pb.quotecast_pb2 import Credentials

# USER_TOKEN SETUP
user_token = YOUR_TOKEN

# API SETUP
credentials=Credentials(user_token=user_token)
api = API(credentials=credentials)

# CONNECTION
api.connection_storage.connect()

# DISPLAY SESSION_ID
session_id = api.connection_storage.session_id

print(session_id)
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