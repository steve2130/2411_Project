import sys

# because I can only use Python 3.7 on UDS -Tommy
if sys.version_info >= (3, 8):
    from typing import TypedDict, Literal, overload  # pylint: disable=no-name-in-module
else:
    from typing_extensions import TypedDict, Literal, overload


class OrdersModel(TypedDict):
    ID:             int
    USER_ID:        int
    ADDRESS_ID:     int
    TOTAL_AMOUNT:   int
    REMARK:         str
    PAID_AT:        str     # timestamp
    PAYMENT_METHOD: str
    PAYMENT_NO:     str
    SHIPMENT_STATUS:str
    SHIPMENT_DATA:  str
    REFUND_STATUS:  str
    REFUND_NO:      str
    CLOSED:         str     # char
