from enum import StrEnum


class OrderAction(StrEnum):
    """Order book action types"""
    ADD = "A"
    CANCEL = "C"
    MODIFY = "M"
    CLEAR = "R"
    TRADE = "T"
    FILL = "F"
    NONE = "N"


class OrderSide(StrEnum):
    """Order side"""
    BID = "B"
    ASK = "A"
    NONE = "N"


