from enum import Enum
from typing import Optional, List

from pydantic import BaseModel


class TaskType(str, Enum):
    SELL = "sell"
    SELL_RETURN = "sellReturn"
    OPEN_SHIFT = "openShift"
    CLOSE_SHIFT = "closeShift"
    SELL_CORRECTION = "sellCorrection"
    BUY_CORRECTION = "buyCorrection"
    SELL_RETURN_CORRECTION = "sellReturnCorrection"
    BUY_RETURN_CORRECTION = "buyReturnCorrection"


class TaxationType(str, Enum):
    OSN = "osn"
    USN_INCOME = "usIncome"
    USN_INCOME_OUTCOME = "usnIncomeOutcome"
    ESN = "esn"


class OperatorModel(BaseModel):
    name: str
    vatin: str


class ItemType(str, Enum):
    POSITION = "position"


class PaymentMethodType(str, Enum):
    FULL_PREPAYMENT = "fullPrepayment"
    FULL_PAYMENT = "fullPayment"
    PREPAYMENT = "prepayment"


class PaymentObjectType(str, Enum):
    COMMODITY = "commodity"
    JOB = "job"
    SERVICE = "service"


class TaxType(str, Enum):
    NONE = "none"
    VAT0 = "vat0"
    VAT10 = "vat10"
    VAT110 = "vat110"
    VAT20 = "vat20"
    VAT120 = "vat120"


class TaxModel(BaseModel):
    type: TaxType
    sum: Optional[float]


class ItemModel(BaseModel):
    type: ItemType
    name: str
    price: float
    quantity: float
    amount: float
    paymentMethod: PaymentMethodType
    paymentObject: PaymentObjectType
    tax: TaxModel


class PaymentType(str, Enum):
    CASH = "cash"
    ELECTRONICALLY = "electronically"


class PaymentModel(BaseModel):
    type: PaymentType
    sum: float


class ClientInfo(BaseModel):
    emailOrPhone: str
    address: Optional[str]
    vatin: Optional[str]
    name: Optional[str]


class TaskRequestModel(BaseModel):
    type: TaskType
    electronically: bool = False
    clientInfo: Optional[ClientInfo]
    taxationType: Optional[TaxationType]
    operator: Optional[OperatorModel]
    items: Optional[List[ItemModel]]
    payments: Optional[List[PaymentModel]]
