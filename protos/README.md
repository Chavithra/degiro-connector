# 1. **Degiro Connector : `Protocol Buffer`**

The data models of this library are mostly built using `Protocol Buffer`.

## 1.1. Which requirements ?
To use `Protocol buffer` the following library are required :
- grpcio
- grpcio-tools
- protobuf

## 1.2. Where are the models ?

The models are in two parts:
- `.proto` files : which define them in `proto3` syntax
- `.py` files : which are generated from the `.proto` files 

`Protocol Buffer` definition files :
- protos\degiro_connector\trading\models\trading.proto

`Python` files :
- degiro_connector.quotecast.models
- degiro_connector.trading.models.trading_pb2.py
- degiro_connector.trading.models.trading_pb2_grpc.py


## 1.3. How to generate the models ?

Here is the command to build the models :

```bash
python -m grpc_tools.protoc \
    --python_out=. \
    --grpc_python_out=. \
    --proto_path=protos \
    --mypy_out=. \
    protos\degiro_connector\trading\models\trading.proto
```

This command will generate the following files :

- degiro_connector.trading.models.trading_pb2.py
- degiro_connector.trading.models.trading_pb2_grpc.py


## 1.4. Workflow : new model

Here is the workflow to add a model called `NewModel` inside `trading` :
- Define it in either `trading.proto` file :

```
message NewModel {
  int32 first_value = 1;
  string second_value = 2;
  double third_value = 3;
  bool fourth_value = 4;
}
```

- Rebuild the `python` models using the right command :

```bash
python -m grpc_tools.protoc \
    --python_out=. \
    --grpc_python_out=. \
    --proto_path=protos \
    --mypy_out=. \
    protos\degiro_connector\trading\models\trading.proto
```

- Import and use the model.

```python
from degiro_connector.trading.models.trading_pb2 import NewModel

new_model = NewModel()
new_model.first_value = 123
new_model.second_value = "Something"
new_model.third_value = 3.14
new_model.fourth_value = True

print(new_model.first_value)
```

# 2. Models definition
A complete guide about `Protocol buffer` definition :

https://developers.google.com/protocol-buffers/docs/proto3


# 3. Models usage

A complete guide about `Protocol buffer` for `python` is available here :

https://developers.google.com/protocol-buffers/docs/pythontutorial

## 3.1. How to set the values ?
Here we will take the example of Credentials to explain how to import and use a model.

Here is the defintion of `Credentials` in the file `trading.proto` :

```
message Credentials {
  int32 int_account = 1;
  string username = 2;
  string password = 3;
  
  oneof oneof_2fa {
    string totp_secret_key = 4;
    int32 one_time_password = 5;
  }
}
```

Here is an example on how to set a model values :
```python
from degiro_connector.trading.models.trading_pb2 import Credentials

credentials = Credentials()
credentials.int_account = 123
credentials.username = "Some user"
credentials.password = "Some password"
credentials.totp_secret_key = "Some secret key"
```


## 3.2. How to access the values ?

Here is an example on how to access a model values :
```python
int_account = credentials.int_account
username = credentials.username
password = credentials.password
totp_secret_key = credentials.totp_secret_key
```

## 3.3. How to convert a model to a dict ?

Here is how to convert a model into a dict :

```python
import degiro_connector.core.helpers.pb_handler as pb_handler

credentials_dict = pb_handler.message_to_dict(message=credentials)
```