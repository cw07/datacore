from enum import StrEnum
from abc import ABC
from ...models.assets import AssetType
from ...models.execution.algo import BaseExecutionAlgo



class OrderSide(StrEnum):
    BUY = "BUY"
    SELL = "SELL"

    @property
    def short_name(self):
        mapping = {
            OrderSide.BUY: "B",
            OrderSide.SELL: "S",
        }
        return mapping[self]

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


class OrderType(StrEnum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"

    @property
    def short_name(self):
        mapping = {
            OrderType.MARKET: "MKT",
            OrderType.LIMIT: "LMT",
        }
        return mapping[self]


    def __str__(self):
        return self.value


    def __repr__(self):
        return self.value


class BaseOrder(ABC):
    """Base order models representing a financial order."""
    order_id: str
    ticker: str
    side: OrderSide
    quantity: float
    order_type: OrderType
    security_type: AssetType
    id_type: str
    price: float
    exec_algo: BaseExecutionAlgo
    strategy: str

    def to_dict(self):
        return self.__dict__