# 1. **Degiro Connector : Extend**

The purpose of this document is to explain how to access or extend this library's features.

## 1.1. How features are grouped ?

Each of the main features of this library fall into one of these two `Python packages` :

|**Package**|**Description**|
|:-|:-|
|`quotecast`|Features providing metrics about financial produccts : `quotecast` or `charts`.|
|`trading`|Features related to trading operations, account or products.|

Notes :
- A `module` is a `Python` file.
- A `package` is a group of `Python` files.

## 1.2. How to access a `quotecast` feature ?

To access features from `quotecast` package you will need an instance of the `API` class from the following module :
- degiro_connector.quotecast.api

Example :

```python
from degiro_connector.quotecast.api import API as QuotecastAPI

quotecast = QuotecastAPI()
quotecast.some_feature(param1, param2...)
quotecast.another_feature(param1, param2...)
```

## 1.3. How to access a `trading` feature ?

To access features from `trading` package you will need an instance of the `API` class from the following module :
- degiro_connector.trading.api

Example :
```python
from degiro_connector.trading.api import API as TradingAPI

trading = TradingAPI()
trading.some_feature(param1, param2...)
trading.another_feature(param1, param2...)
```

## 1.4. Concrete example : `get_config`
Let's take a look the feature `get_config` from `trading`.

Here is how to call this method :
```python
from degiro_connector.trading.api import API as TradingAPI

quotecast.get_config()
```

# 2. `Actions` : add / change

We saw how to access a feature now lets see how to add/change one.

## 2.1. Where are the feature ?
Each feature has it's own Action file.

Here is the generic location of an Action modules :

|**Package**|**Location of actions**|
|:-|:-|
|`quotecast`|`degiro_connector.quotecast.actions.<action_name>`|
|`trading`|`degiro_connector.trading.actions.<action_name>`|

## 2.2. What is an `Action` ?
An `Action` is a class which extends from :
|**Class**|**Module**|
|:-|:-|
|`AbstractActions`|`degiro_connector.core.abstracts.abstract_action`|

## 2.2. How to add an `Action` ?

You want to add an `Action` called `some_feature` inside `trading` category.

Here is the workflow to do so :
- create a module : `degiro_connector.trading.actions.action_some_feature`
- define a class : `ActionSomeFeature`
- extends this class from `AbstractAction`

Here is an example of code :

```python
# FILE : degiro_connector/trading/actions/action_some_feature.py

from degiro_connector.core.abstracts.abstract_action import AbstractAction

class ActionSomeFeature(AbstractAction):
    def call(self) -> str:
        return "something"
```

Usage :
```python
from degiro_connector.trading.api import API as TradingAPI

trading = TradingAPI()
trading.some_feature()
```

## 2.3. Which parameters can I get ?

`AbstractAction` provide some attributes and methods by default.

Parameters available inside an `Action` :

|**Attribute**|**Description**|
|:-|:-|
|credentials|contains login credentials|
|connection_storage|contains session_id|
|session_storage|contains requests.Session object|
|build_session|build a requests.Session object|
|build_logger|build a logging.Logger object|

Example :

```python
# FILE : degiro_connector/quotecast/actions/action_some_feature.py

class ActionSomeFeature(AbstractAction):
    def call(self):
        credentials = self.credentials
        session_id = self.connection_storage.session_id
        connected = self.connection_storage.connected
        timeout = self.connection_storage.timeout
        session = self.session_storage.session
        new_session = self.build_session()
        new_logger = self.build_logger()