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
    GET_DEVICE_STATUS = "getDeviceStatus"


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
    PREPAYMENT = "prepayment"
    ADVANCE = "advance"
    FULL_PAYMENT = "fullPayment"
    PARTIAL_PAYMENT = "partialPayment"
    CREDIT = "credit"
    CREDIT_PAYMENT = "creditPayment"


class PaymentObjectType(str, Enum):
    COMMODITY = "commodity"
    JOB = "job"
    SERVICE = "service"
    PAYMENT = "payment"
    DEPOSIT = "deposit"


class TaxType(str, Enum):
    NONE = "none"
    VAT0 = "vat0"
    VAT10 = "vat10"
    VAT110 = "vat110"
    VAT20 = "vat20"
    VAT120 = "vat120"


class MeasurementUnitType(str, Enum):
    PIECE = "piece"
    GRAM = "gram"
    KILOGRAM = "kilogram"
    TON = "ton"
    CENTIMETER = "centimeter"
    DECIMETER = "decimeter"
    METER = "meter"
    SQUARE_CENTIMETER = "squareCentimeter"
    SQUARE_DECIMETER = "squareDecimeter"
    SQUARE_METER = "squareMeter"
    MILLIMETER = "millimeter"
    LITER = "liter"
    CUBIC_METER = "cubicMeter"
    KILOWATT_HOUR = "kilowattHour"
    GKAL = "gkal"
    DAY = "day"
    HOUR = "hour"
    MINUTE = "minute"
    SECOND = "second"
    KILOBYTE = "kilobyte"
    MEGABYTE = "megabyte"
    GIGABYTE = "gigabyte"
    TERABYTE = "terabyte"
    OTHER_UNITS = "otherUnits"


class CorrectionType(str, Enum):
    SELF = "self"
    INSTRUCTION = "instruction"


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
    measurementUnit: Optional[MeasurementUnitType]


class PaymentType(str, Enum):
    CASH = "cash"
    ELECTRONICALLY = "electronically"
    PREPAID = "prepaid"
    CREDIT = "credit"


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

    correctionType: Optional[CorrectionType]
    correctionBaseDate: Optional[str]
    correctionBaseNumber: Optional[str]
    paymentsPlace: Optional[str]
    paymentsAddress: Optional[str]
    machineNumber: Optional[str]
