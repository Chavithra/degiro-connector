class MessageRegistration:
    metric_name: str  # f"{product_id}.{metric_type}""
    reference: int

    def __init__(self, metric_name, reference):
        self.metric_name = metric_name
        self.reference = reference

    def __repr__(self) -> str:
        return f"`{self.reference}`:`{self.metric_name}`"


class MessageUnregistration:
    metric_name: str
    reference: int

    def __init__(self, metric_name, reference):
        self.metric_name = metric_name
        self.reference = reference

    def __repr__(self) -> str:
        return f"`{self.reference}`:`{self.metric_name}`"


class MessageNumeric:
    reference: int
    value: float

    def __init__(self, reference, value):
        self.reference = reference
        self.value = value

    def __repr__(self) -> str:
        return f"`{self.reference}`:`{self.value}`"


class MessageText:
    reference: int
    value: str

    def __init__(self, reference, value):
        self.reference = reference
        self.value = value

    def __repr__(self) -> str:
        return f"`{self.reference}`:`{self.value}`"


# A message from the list of messages received from Degiro's Quotecast API.
Message = MessageRegistration | MessageUnregistration | MessageNumeric | MessageText
