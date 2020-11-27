import datetime
import logging
import orjson as json

from quotecast.models.metrics_storage import MetricsStorage
from quotecast.pb.quotecast_pb2 import Quotecast, Ticker
from typing import Dict
from wrapt.decorators import synchronized

class QuotecastParser:
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
        * VWID
        * LABEL

    The REFERENCE is a unique identifier in Degiro's Quotecast API
    which refers to the financial data.

    The VALUE is the value of the financial data.

    THE VWID is the id of the product (etf, option, stock, warrant...)
    from which we retrieve measurements (LastPrice, LastVolume...).

    The LABEL is the name of the measurements that we retrieve.

    The MATCHING table is only sent at the first call of this endpoint.


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
        * "d" : rejected subscription
        * "ue" : data not available
        * "un" : numeric data
        * "us" : string data
        * ... (this list may not be exhaustive)

    Depending on the MESSAGE_TYPE different kind of information are stored
    inside :
        * CODE1
        * CODE2

    If MESSAGE_TYPE = "a_req" or "a_rel" :
        * CODE1 : contains the product's VWID and the PARAMETER_NAME.
        * CODE2 : contains the REFERENCE for the parameter in CODE1.
        * Example of MESSAGE : 
        ```json
        {
            "m": "a_req",
            "v": ["365004197.B10Volume", 624239]
        }
        ```
        "365004197.B10Volume" <=> CODE1
        365004197 <=> VWID
        B10Volume <=> PARAMETER_NAME
        624239 <=> REFERENCE

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
        624239 <=> CODE1
        115.85 <=> CODE2
    """

    @staticmethod
    def build_ticker_from_quotecast(
        quotecast:Quotecast,
        ticker:Ticker=Ticker(),
        references:Dict[int, float]=dict(),
    ):
        # SETUP PRODUCTS & METRICS
        parsed_json = json.loads(quotecast.json_data)
        for data in parsed_json:
            if  data['m'] == 'un' :
                reference = data['v'][0]
                value = data['v'][1]
                product, name = references[reference].split('.')
                ticker.products[int(product)].metrics[name] = value
            elif data['m'] == 'us':
                reference = data['v'][0]
                value = data['v'][1]
                product, name = references[reference].split('.')
                if value[4] == '-':
                    date = datetime.datetime.strptime(
                        value,
                        '%Y-%m-%d',
                    )
                    value = datetime.datetime.timestamp(date)
                elif value[2] == ':':
                    time = datetime.time.fromisoformat(value)
                    value = time.hour * 3600 + time.minute * 60 + time.second
                ticker.products[int(product)].metrics[name] = value
            elif data['m'] == 'a_req':
                references[data['v'][1]] = data['v'][0]
            elif data['m'] == 'a_rel':
                delete_list = []
                for reference in references:
                    if references[reference] == data['v'][0]:
                        delete_list.append()

                for element in delete_list:
                    del references[element]
            elif data['m'] == 'h':
                pass
            elif data['m'] == 'ue':
                pass
            elif data['m'] == 'd':
                raise AttributeError(f'Subscription rejected : {data}')
            else:
                raise AttributeError(f'Unknown metric : {data}')

        # SETUP PRODUCT LIST
        ticker.product_list.extend(ticker.products)

        # SETUP METADATA
        ticker.metadata.MergeFrom(quotecast.metadata)

        return ticker

    @property
    def references(self)->Dict[int, str]:
        return self.__references

    @property
    def ticker(self)->Ticker:
        return self.__ticker

    def __init__(self, forward_fill:bool=False):
        """
        Args:
            forward_fill (bool, optional):
                Whether or not we want to fill the new Ticker with
                previous received metrics.
        """

        self.__forward_fill = forward_fill
        self.__metrics_storage = MetricsStorage()
        self.__references = dict()
        self.__ticker = Ticker()

        self.__logger = logging.getLogger(self.__module__)

    def put_quotecast(self, quotecast:Quotecast):
        forward_fill = self.__forward_fill
        metrics_storage = self.__metrics_storage
        references = self.__references

        ticker = self.build_ticker_from_quotecast(
            quotecast=quotecast,
            ticker=Ticker(),
            references=references,
        )

        if forward_fill == True:
            metrics_storage.fill_ticker(ticker=ticker)

        self.__ticker = ticker

if __name__ == '__main__':
    data = '[{"m":"h"},{"m":"a_req","v":["360015751.LastPrice",101]},{"m":"un","v":[101,119.900000]}]'