import datetime
import logging
import json
import pandas as pd

from degiro_connector.quotecast.models.metrics_storage import MetricsStorage
from degiro_connector.quotecast.models.quotecast_pb2 import Quotecast, Ticker
from typing import Dict, List, Union


class QuotecastParser:
    """Handle the payload returned from this endpoint :

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
        * VWD_ID
        * LABEL

    The REFERENCE is a unique identifier in Degiro's Quotecast API
    which refers to the financial data.

    The VALUE is the value of the financial data.

    THE VWD_ID is the id of the product (etf, option, stock, warrant...)
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
        'm': MESSAGE_TYPE
        'v': [CODE1, CODE2]
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
        * "h" : heartbeat
        * "sr" : session invalid
        * "ue" : data not available
        * "un" : numeric data
        * "us" : string data
        * ... (this list may not be exhaustive)

    Depending on the MESSAGE_TYPE different kind of information are stored
    inside :
        * CODE1
        * CODE2

    If MESSAGE_TYPE = "a_req" or "a_rel" :
        * CODE1 : contains the product's VWD_ID and the PARAMETER_NAME.
        * CODE2 : contains the REFERENCE for the parameter in CODE1.
        * Example of MESSAGE :
        ```json
        {
            "m": "a_req",
            "v": ["365004197.B10Volume", 624239]
        }
        ```
        "365004197.B10Volume" <=> CODE1
        365004197 <=> VWD_ID
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

    @classmethod
    def ticker_to_df(
        cls,
        ticker: Ticker,
        column_list: List[str] = None,
    ) -> pd.DataFrame:
        """Converts a ticker to a "pandas.DataFrame".
        Args:
            ticker (Ticker):
                Ticker to convert.
            column_list (List[str]):
                Mandatory fields : will be set to "None" if empty.
                Default to [].
        Returns:
            pandas.DataFrame:
                "pandas.DataFrame" containing the metrics.
                Each row depicts a specific product.
                Each column depicts a specific metric.
        """

        if column_list is None:
            column_list = list()

        ticker_dict = cls.ticker_to_dict(
            ticker=ticker,
            column_list=column_list,
        )

        df = pd.DataFrame(ticker_dict.values())

        return df

    @staticmethod
    def ticker_to_dict(
        ticker: Ticker,
        column_list: List[str] = None,
    ) -> Dict[str, Dict[str, Union[str, int]]]:
        # VWD_ID  # METRICS : NAME / VALUE
        """Converts a ticker to a "dict".
        Args:
            ticker (Ticker):
                Ticker to convert.
            column_list (List[str]):
                Mandatory fields : will be set to "None" if empty.
                Default to [].
        Returns:
            Dict[Union[str, int], Dict[str, Union[str, int]]]:
                Dict containing all the metrics grouped by "vwd_id".
        """

        if column_list is None:
            column_list = list()

        empty_list = [None] * len(column_list)
        empty_metrics = dict(zip(column_list, empty_list))
        empty_metrics[
            "response_datetime"
        ] = ticker.metadata.response_datetime.ToJsonString()
        empty_metrics["request_duration"] = (
            ticker.metadata.request_duration.ToMicroseconds() / 10 ** 6
        )

        ticker_dict:Dict[str, Dict[str, Union[str, int]]] = dict()
        for product in ticker.products:
            ticker_dict[product] = empty_metrics.copy()
            ticker_dict[product]["vwd_id"] = product
            ticker_dict[product].update(ticker.products[product].metrics)

        return ticker_dict

    @staticmethod
    def build_ticker_from_quotecast(
        quotecast: Quotecast,
        references: Dict[int, List[str]] = None,
        ticker: Ticker = None,
    ) -> Ticker:
        """Build or update a Ticker metrics using a Quotecast object.

        Only the metrics which can be converted to float are supported.

        But that should be enough to handle all the real use cases.

        This was done to :
            * Keep the Ticker structure simple and light.
            * Have better performances during processing.

        Args:
            quotecast (Quotecast):
                Object containing the raw metrics.
            ticker (Ticker, optional):
                Object to update with the new metrics.
                Defaults to Ticker().
            references (Dict[int, List[str]], optional):
                The references dictionnary is a registry.
                It links the products :
                    * reference
                    * vwd_id
                    * metric
                Here is an example of how to populate it :
                    references[reference] = [vwd_id, metric]
                Defaults to dict().

        Raises:
            AttributeError:
                If the subscription is rejected.
                Or if the metric is unknown.

        Returns:
            Ticker: New or updated Ticker.
        """

        if references is None:
            references = dict()

        if ticker is None:
            ticker = Ticker()

        # SETUP PRODUCTS & METRICS
        message_array = json.loads(quotecast.json_data)
        for message in message_array:
            if message["m"] == "un":
                reference = message["v"][0]
                value = message["v"][1]
                product, metric = references[reference]
                ticker.products[product].metrics[metric] = value
            elif message["m"] == "us":
                reference = message["v"][0]
                value = message["v"][1]
                product, metric = references[reference]

                if value[4] == "-":
                    date = datetime.datetime.strptime(
                        value,
                        "%Y-%m-%d",
                    )
                    value = datetime.datetime.timestamp(date)
                    ticker.products[product].metrics[metric] = value
                elif value[2] == ":":
                    time = datetime.time.fromisoformat(value)
                    value = time.hour * 3600 + time.minute * 60 + time.second
                    ticker.products[product].metrics[metric] = value
                else:
                    # NOT CONVERTIBLE TO FLOAT
                    raise RuntimeWarning(
                        "Unsupported string metric : " f"{metric} = {message}"
                    )
            elif message["m"] == "a_req":
                references[message["v"][1]] = message["v"][0].rsplit(
                    sep=".",
                    maxsplit=1,
                )
            elif message["m"] == "a_rel":
                delete_list = []
                for reference in references:
                    if ".".join(references[reference]) == message["v"][0]:
                        delete_list.append(reference)

                for reference in delete_list:
                    del references[reference]
            elif message["m"] == "h":
                pass
            elif message["m"] == "ue":
                pass
            elif message["m"] == "d":
                raise AttributeError(f"Subscription rejected : {message}")
            else:
                raise AttributeError(f"Unknown metric : {message}")

        # SETUP PRODUCT LIST
        ticker.product_list.extend(ticker.products)

        # SETUP METADATA
        ticker.metadata.MergeFrom(quotecast.metadata)

        return ticker

    @property
    def references(self) -> Dict[int, List[str]]:
        return self.__references

    @property
    def ticker(self) -> Ticker:
        return self.__ticker

    @property
    def ticker_df(self) -> pd.DataFrame:
        ticker = self.__ticker
        ticker_df = self.ticker_to_df(ticker=ticker)
        return ticker_df

    @property
    def ticker_dict(
        self,
    ) -> Dict[str, Dict[str, Union[str, int]]]:
        # VWD_ID  # METRICS : NAME / VALUE
        ticker = self.__ticker
        ticker_dict = self.ticker_to_dict(ticker=ticker)
        return ticker_dict

    def __init__(self, forward_fill: bool = False):
        """
        Args:
            forward_fill (bool, optional):
                Whether or not we want to fill the new Ticker with
                previous received metrics.
                Default to False.
        """

        self.__forward_fill = forward_fill
        self.__metrics_storage = MetricsStorage()
        self.__references:Dict[int, List[str]] = dict()
        self.__ticker = Ticker()

        self.__logger = logging.getLogger(self.__module__)

    def put_quotecast(self, quotecast: Quotecast):
        forward_fill = self.__forward_fill
        metrics_storage = self.__metrics_storage
        references = self.__references

        ticker = self.build_ticker_from_quotecast(
            quotecast=quotecast,
            ticker=Ticker(),
            references=references,
        )

        if forward_fill is True:
            metrics_storage.fill_ticker(ticker=ticker)

        self.__ticker = ticker

    def rebuild_request(self) -> Quotecast.Request:
        """Rebuild the request from history (self.__references).

        Returns:
            Quotecast.Request:
                Request matching data-stream.
        """

        references = self.references
        request = Quotecast.Request()

        for vwd_id, metric in references.values():
            request.subscriptions[vwd_id].append(metric)

        return request


if __name__ == "__main__":
    data = (
        '[{"m":"h"},{"m":"a_req","v":["360015751.LastPrice",101]},'
        '{"m":"un","v":[101,119.900000]}]'
    )
