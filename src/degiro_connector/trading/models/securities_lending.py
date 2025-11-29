from datetime import date as Date

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

class SecuritiesLendingStatus(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        extra="allow",
        populate_by_name=True,
    )

    status: str
    is_available: bool

class SecuritiesLending(BaseModel):
    data: SecuritiesLendingStatus

class SecuritiesLendingReportDateItem(BaseModel):
    """Model for securities lending report date item.
    
    Note: Pydantic automatically parses ISO format date strings (YYYY-MM-DD)
    during deserialization/validation when converting from JSON or dict data.
    """
    model_config = ConfigDict(
        alias_generator=to_camel,
        extra="allow",
        populate_by_name=True,
    )

    date: Date

class SecuritiesLendingReportDate(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        extra="allow",
        populate_by_name=True,
    )

    data: SecuritiesLendingReportDateItem

class SecuritiesLendingReportPosition(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        extra="allow",
        populate_by_name=True,
    )

    accrual: float
    accrual_ccy: str
    custodian: str
    initial_accrual: float
    isin: str
    lending_rate: float
    loan_id: str
    loan_value: float
    loan_value_ccy: str
    market_value: float
    market_value_ccy: str
    price: float
    price_ccy: str
    product_id: str
    quantity: int
    revenue_status: str
    value: float

class SecuritiesLendingReportSnapshotItem(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        extra="allow",
        populate_by_name=True,
    )

    accrual: float
    accrual_ccy: str
    client_id: str
    collateral_value: float
    collateral_value_ccy: str
    earning_to_date: float
    earning_to_date_ccy: str
    initial_accrual: float
    position_value: float
    position_value_ccy: str
    positions: list[SecuritiesLendingReportPosition] = Field(default_factory=list)

class SecuritiesLendingReportSnapshot(BaseModel):
    data: list[SecuritiesLendingReportSnapshotItem] = Field(default_factory=list)