import json
import logging

from quotecast.pb.quotecast_pb2 import (
    Matching,
    Metric,
)
from typing import List

""" Handle the payload returned from this endpoint :

"https://degiro.quotecast.vwdservices.com/CORS/{session_id}"


OVERALL EXPLANATION
The endpoint aforementioned returns financial data measurement
such as :
    * LastPrice of a Stock
    * LastVolume of a Stock
    * ...

This endpoint use HTTP 1.1 protocol.

Since there are no way to retrieve data asynchronously from
HTTP 1.1, this endpoint uses Long-Polling method to retrieve data
as soon as they are available.

Thus to consume this endpoint one needs to recall it as soon as a
response has been received.

If no data updates are available a HEARTBEAT signal is sent every
5 seconds.

The session timeout is approximativaly 15 seconds.


PAYLOAD DATA DESCRIPTION
The payload sent from this endpoint can contain three kind of
objects :
    * DATA
    * HEARTBEAT
    * MATCHING

A DATA is an object with two elements :
    * REFERENCE
    * VALUE

A HEARTBEAT is signal sent every 5 seconds if no data updates
are available.

A MATCHING is an object with three elements :
    * REFERENCE
    * PRODUCT_ID
    * LABEL

The REFERENCE is a unique identifier in Degiro's Quotecast API
which refers to the financial data.

The VALUE is the value of the financial data.

THE PRODUCT_ID is the id of the product (etf, option, stock,
warrant...) from which we retrieve measurements (LastPrice...).

The LABEL is the name of the measurements that we retrieve.

The MATCHING table is only sent the time we call this endpoint


PAYLOAD DATA STRUCTURE
The payload is a list of messages serialized in JSON, as follows :
```json
[
    MESSAGE_1,
    MESSAGE_2,
    ...
    MESSAGE_X
]
```

What is called a MESSAGE here above, is an object with the two
attributes :
    * "m"
    * "v"

We can denote a message like this :
```python
MESSAGE = {
    'm' : MESSAGE_TYPE
    'v' : [CODE1, CODE2]
}
```

Here we have the following properties:
    * m contains a MESSAGE_TYPE
    * MESSAGE_TYPE is a str
    * v is a list
    * v contains 2 elements
    * CODE1 is a str or an int
    * CODE2 is a float

The MESSAGE_TYPE indicate the type of message, it can take the
following __values :
    * "a_req"
    * "a_rel"
    * "un"
    * "us"
    * ... (this list is not exhaustive)

Depending on the MESSAGE_TYPE different kind of information are stored
inside :
    * CODE1
    * CODE2

If MESSAGE_TYPE = "a_req" or "a_rel" :
    * CODE1 : contains the financial PRODUCT'S ID and the PARAMETER'S
    NAME.
    * CODE2 : contains the reference for the parameter in CODE1.
    * Example of MESSAGE : 
    ```json
    {
        "m": "a_req",
        "v": ["365004197.B10Volume", 624239]
    }
    ```
    "365004197.B10Volume" is the CODE1
    365004197 is the financial PRODUCT'S ID
    B10Volume is the PARAMETER'S NAME
    624239 is the CODE2

If MESSAGE_TYPE = "un" or "us :
    * CODE1 : contains the reference number.
    * CODE2 : contains the value of the information referenced by
    CODE1.
    * Example of MESSAGE : 
    ```json
    {
        "m": "a_req",
        "v": [624239, 115.85]
    }
    ```
    624239 is the CODE1
    115.85 is the CODE2
"""


def __has_valid_m(
    mv:dict,
)->bool:
    """ Check if "m" is built well enough to be parsed. """
    valid = isinstance(mv, dict) and 'm' in mv

    if valid and mv['m'] == 'h':
        return True

    return valid \
    and isinstance(mv['m'], str)


def __has_valid_v(
    mv:dict,
)->bool:
    """ Check if "v" is built well enough to be parsed. """
    
    return isinstance(mv, dict) \
    and 'v' in mv \
    and isinstance(mv['v'], list) \
    and len(mv['v']) == 2


def __update_matching_list(
    matching_list:List[Matching],
    metric_list:List[Metric],
    mv:dict,
):

    if not __has_valid_v(mv):
        raise AttributeError
    elif mv['m'] == 'a_rel':
        product_id, label = mv['v'][0].split('.')

        for matching in matching_list:
            if matching.product_id == product_id \
            and matching.label == label :
                matching_list.remove(matching)
    elif mv['m'] == 'a_req':
        #action = mv['m']
        product_id, label = mv['v'][0].split('.')
        reference = mv['v'][1]

        matching = Matching(
            label=str(label),
            product_id=int(product_id),
            reference=int(reference)
        )

        if matching in matching_list:
            matching_list.remove(matching)
        
        matching_list.append(matching)


def __update_metric_list(
    matching_list:List[Matching],
    metric_list:List[Metric],
    mv:dict,
):

    if mv['m'] == 'h':
        metric_list.append(Metric(heartbeat=True))
    elif not __has_valid_v(mv):
        raise AttributeError
    else:
        #action = mv['m']
        reference = mv['v'][0]
        value = mv['v'][1]

        product_id = 0
        label = ''
        for matching in matching_list:
            if matching.reference == reference:
                label = matching.label
                product_id = matching.product_id

        metric_list.append(
            Metric(
                reference=int(reference),
                value=str(value),
                product_id=int(product_id),
                label=str(label)
            )
        )


def build_metric_list_from_json(
    json_data:str,
    matching_list:List[Matching]=None,
)->(List[Matching], List[Metric]):
    """ Takes Degiro's Quotecast API payload and build a list of Metric
    objects.

    Args:
        json_data (str):
            API payload in JSON format.
        matching_list (List[Matching], optional):
            List of Matching objects extract from previous payload.

    Raises:
        AttributeError

    Returns:
        List[Matching]:
            List of Matching objects extracted.
        List[Metric]:
            List of Matching objects extracted.
    """

    data = json.loads(json_data)
    if matching_list is None : matching_list = []
    metric_list=[]

    for mv in data:
        if not __has_valid_m(mv=mv):
            raise AttributeError
        elif mv['m'] in ['a_rel', 'a_req']:
            __update_matching_list(
                matching_list=matching_list,
                metric_list=metric_list,
                mv=mv,
            )
        elif mv['m'] in ['h', 'us', 'un']:
            __update_metric_list(
                matching_list=matching_list,
                metric_list=metric_list,
                mv=mv,
            )

    return (matching_list, metric_list)


def extract_product_list(
    metric_list,
)->List[int]:
    metric_list = metric_list

    product_list = list()
    for metric in metric_list:
        if not metric.product_id in product_list:
            product_list.append(metric.product_id)

    return product_list

if __name__ == '__main__':
    data = '[{"m":"h"},{"m":"a_req","v":["360015751.LastPrice",101]},{"m":"un","v":[101,119.900000]}]'
    (matching_list, metric_list) = build_metric_list_from_json(data)

    print(matching_list, metric_list)