import logging
import orjson as json

from quotecast.pb.quotecast_pb2 import (
    Metric,
)
from typing import Dict, List, Union



class RawMetricParser:
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
        * "a_req" : subscription
        * "a_rel" : unsubscription
        * "un" : data
        * "us" : data
        * "d" : rejected subscription
        * "ue" : ?
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

    @staticmethod
    def is_valid_m(raw_metric:dict)->bool:
        """ Check if "m" is built well enough to be parsed. """
        if  isinstance(raw_metric, dict) \
            and 'm' in raw_metric \
            and isinstance(raw_metric['m'], str):
            return True
        else:
            return False

    @staticmethod
    def is_valid_v(raw_metric:dict)->bool:
        """ Check if "v" is built well enough to be parsed. """
        
        if  isinstance(raw_metric, dict) \
            and 'v' in raw_metric \
            and isinstance(raw_metric['v'], list) \
            and len(raw_metric['v']) == 2:
            return True
        else:
            return False

    @property
    def matching_list(self)->Dict[int, Dict[str, Union[int, str]]]:
        return self.__matching_list

    @property
    def metric_list(self)->List[Metric]:
        return self.__metric_list

    def __init__(self):
        self.__logger = logging.getLogger(self.__module__)
        self.__matching_list = dict()
        self.__metric_list = list()

    def put_raw_metric_list(self, raw_json:str):
        self.__metric_list = []

        raw_metric_list = json.loads(raw_json)

        if not isinstance(raw_metric_list, list):
            raise AttributeError('No metrics list inside "raw_json".')

        else:
            for raw_metric in raw_metric_list:
                self.put_raw_metric(raw_metric=raw_metric)

    def put_raw_metric(self, raw_metric:dict):
        logger = self.__logger

        if not self.is_valid_m(raw_metric=raw_metric):
            raise AttributeError('Invalid "raw_metric" dict.')

        elif raw_metric['m'] in ['a_rel', 'a_req']:
            self.update_matching(raw_metric=raw_metric)

        elif raw_metric['m'] in ['h', 'us', 'un']:
            self.update_metric(raw_metric=raw_metric)

        elif raw_metric['m'] in ['d']:
            logger.fatal(f'Can\'t subscribe to : {raw_metric}')

        else:
            logger.fatal(f'Unknown "raw_metric" : {raw_metric}')

    def update_metric(self, raw_metric:dict)->Metric:
        matching_list = self.__matching_list
        metric_list = self.__metric_list

        if raw_metric['m'] == 'h':
            metric = Metric(heartbeat=True)

        elif not self.is_valid_v(raw_metric=raw_metric):
            raise AttributeError('Invalid "raw_metric" dict.')

        elif raw_metric['m'] in ['us', 'un']:
            reference = raw_metric['v'][0]
            value = raw_metric['v'][1]
            matching = matching_list[reference]
            label = matching['label']
            product_id = matching['product_id']

            metric = Metric(
                reference=int(reference),
                value=str(value),
                product_id=int(product_id),
                label=str(label),
            )

            metric_list.append(metric)

        else:
            raise AttributeError('Unknown "raw_metric" dict.')
        
        
        return metric

    def update_matching(self, raw_metric:dict):
        matching_list = self.__matching_list
        
        if not self.is_valid_v(raw_metric=raw_metric):
            raise AttributeError('Invalid "raw_metric" dict.')
        
        elif raw_metric['m'] == 'a_req':
            product_id, label = raw_metric['v'][0].split('.')
            reference = raw_metric['v'][1]

            matching_list[reference] = {
                'label':str(label),
                'product_id':int(product_id),
            }

        elif raw_metric['m'] == 'a_rel':
            product_id, label = raw_metric['v'][0].split('.')

            reference_list = list()
            for reference, matching in matching_list.items():
                if  matching['product_id'] == product_id \
                    and matching['label'] == label:
                    reference_list.append(reference)
            
            if len(reference_list) >0:
                for reference in reference_list:
                    del matching_list[reference]

if __name__ == '__main__':
    raw_metric_parser = RawMetricParser()
    
    data = '[{"m":"h"},{"m":"a_req","v":["360015751.LastPrice",101]},{"m":"un","v":[101,119.900000]}]'

    raw_metric_parser.put_raw_metric_list(raw_json=data)
    print(raw_metric_parser.matching_list)
    for metric in raw_metric_parser.metric_list:
        print(metric)