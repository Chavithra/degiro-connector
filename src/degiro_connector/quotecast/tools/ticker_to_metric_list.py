import orjson as json


from degiro_connector.quotecast.models.message import (
    Message,
    MessageNumeric,
    MessageRegistration,
    MessageText,
    MessageUnregistration,
)
from degiro_connector.quotecast.models.metric import (
    Metric,
    MetricType,
)
from degiro_connector.quotecast.models.ticker import Ticker


class TickerToMetricList:
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

    @staticmethod
    def from_ticker_to_message_list(ticker: Ticker) -> list[Message]:
        json_text = ticker.json_text
        message_list_raw = json.loads(json_text)  # pylint: disable=no-member
        message_list: list[Message] = []

        for message_raw in message_list_raw:
            if message_raw["m"] == "un":
                message_list.append(
                    MessageNumeric(
                        reference=message_raw["v"][0],
                        value=message_raw["v"][1],
                    ),
                )
            elif message_raw["m"] == "us":
                message_list.append(
                    MessageText(
                        reference=message_raw["v"][0],
                        value=message_raw["v"][1],
                    ),
                )
            elif message_raw["m"] == "a_req":
                message_list.append(
                    MessageRegistration(
                        metric_name=message_raw["v"][0],
                        reference=message_raw["v"][1],
                    ),
                )
            elif message_raw["m"] == "a_rel":
                message_list.append(
                    MessageUnregistration(
                        metric_name=message_raw["v"][0],
                        reference=message_raw["v"][1],
                    ),
                )
            elif message_raw["m"] == "h":
                pass
            elif message_raw["m"] == "ue":
                pass
            elif message_raw["m"] == "d":
                raise AttributeError(
                    f"Subscription rejected, the `vwd_id` or `metric` might not exist. - {message_raw}"
                )
            else:
                raise AttributeError(f"Unknown metric : {message_raw}")

        return message_list

    def __init__(
        self,
        reference_map: dict[int, list] | None = None,
    ) -> None:
        """

        Parameters
        ----------
            reference_map: dict[int, list] | None
                Dictionnary storing the references returned by Degiro's Quotecast.
                Each reference number matches with a specific product/metric_type set.
                Example : {reference_number: [product_id, metric_type]}
        """
        # {reference: [product_id, metric_type]}
        self._reference_map: dict[int, list] = reference_map or {}

    def from_message_list_to_metric_list(
        self, message_list: list[Message]
    ) -> list[Metric]:
        reference_map = self._reference_map
        metric_list = []

        for message in message_list:
            if isinstance(message, MessageRegistration):
                reference_map[message.reference] = message.metric_name.rsplit(
                    sep=".", maxsplit=1
                )
            elif isinstance(message, MessageUnregistration):
                del reference_map[
                    message.reference
                ]  # crashes on purpose to detect inconsistency
            elif isinstance(message, (MessageNumeric, MessageText)):
                product_id, metric_type = reference_map[message.reference]
                metric_list.append(
                    Metric(
                        product_id=product_id,
                        metric_type=MetricType(metric_type),
                        value=message.value,
                    ),
                )

        return metric_list

    def parse(self, ticker: Ticker) -> list[Metric]:
        message_list = self.from_ticker_to_message_list(ticker=ticker)
        metric_list = self.from_message_list_to_metric_list(message_list=message_list)
        return metric_list
