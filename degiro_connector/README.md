# 1. **Degiro Connector : Extension **

The purpose of this document is to explain the extension mechanism of this library.

## 1.1. How to access a feature ?

There are two categories of features :
- `quotecast`
- `trading`

There is a specific module for each category :
- `quotecast` : degiro_connector.quotecast.api
- `trading` : degiro_connector.trading.api

Here is of the access features / methods :
```python
from degiro_connector.quotecast.api import API as QuotecastAPI
from degiro_connector.trading.api import API as TradingAPI

quotecast = QuotecastAPI()
quotecast.some_feature(param1, param2...)
quotecast.another_feature(param1, param2...)


trading = TradingAPI()
trading.some_feature(param1, param2...)
trading.another_feature(param1, param2...)
```

## 1.2. Where are the feature stored ?
Let's take a look the method `get_config` from `trading`.

Here is how to call this method :
```python
from degiro_connector.trading.api import API as TradingAPI

quotecast.get_config()
```

This method is defined in :
- class : `ActionGetConfig`
- module : degiro_connector.trading.actions.action_get_config

# 2. `Actions`

## 2.1. What is an `Action` ?
An `Action` class is a class which extends from :
- class : `AbstractActions`
- module : degiro_connector.core.abstracts.abstract_action

Actions path looks like this :
- quotecast :  `degiro_connector.quotecast.actions.<action_name>`
- trading :  `degiro_connector.trading.actions.<action_name>`

## 2.2. How to add an `Action` ?

You want to add an `Action` called `some_feature` inside `trading` category.

Here is the workflow to do so :
- create a module : `degiro_connector.quotecast.actions.action_some_feature`
- define a class : `ActionSomeFeature`
- extends this class from `AbstractAction`

Here is an example of code :

```python
# FILE : degiro_connector/quotecast/actions/action_some_feature.py

from degiro_connector.core.abstracts.abstract_action import AbstractAction

class ActionSomeFeature(AbstractAction):
    def call(self):
        return "something"
```

## 2.3. Which are the available attributes/methods ?

Inside an `Action` object you can access the followings :
- self.credentials : contains login credentials
- self.connection_storage : contains session_id
- self.session_storage : contains requests.Session object
- self.build_session() : build a requests.Session object
- self.build_logger() : build a logging.Logger object