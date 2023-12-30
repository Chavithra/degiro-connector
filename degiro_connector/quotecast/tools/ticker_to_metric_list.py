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
                raise AttributeError(f"Subscription rejected : {message_raw}")
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
