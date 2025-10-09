from enum import StrEnum


class OrderAction(StrEnum):
    """Order book action types"""
    ADD = "Add"
    CANCEL = "Cancel"
    MODIFY = "Modify"
    CLEAR = "Clear"
    TRADE = "Trade"
    FILL = "Fill"
    NONE = "None"


class OrderSide(StrEnum):
    """Order side"""
    BID = "Bid"
    ASK = "Ask"
    NONE = "None"


