import sys

# because I can only use Python 3.7 on UDS -Tommy
if sys.version_info >= (3, 8):
    from typing import TypedDict, Literal, overload  # pylint: disable=no-name-in-module
else:
    from typing_extensions import TypedDict, Literal, overload


class OrderItemsModel(TypedDict):
    ID:             int
    ORDER_ID:       int
    PRODUCT_ID:     int
    PRODUCT_SKU_ID: int
    AMOUNT:         int
    PRICE:          float
