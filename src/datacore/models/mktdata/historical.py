import datetime as dt
from typing import Optional

from dataclasses import dataclass,fields
from datacore.models.mktdata.base import BaseMarketData
from datacore.models.mktdata.schema import MktDataSchema

@dataclass
class OHLCV1D(BaseMarketData):
    ts_event: str

    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    price: Optional[float] = None
    volume: Optional[float] = None
    rtype: Optional[int] = None
    instrument_id: Optional[int] = None
    publisher_id: Optional[int] = None

    data_schema = MktDataSchema.OHLCV_1D

    def __post_init__(self):
        if self.close is None and self.price is None:
            raise ValueError("At least one of 'close' or 'price' must be provided")

    def db_table_name(self):
        return f"{self.venue}_{self.vendor}_{self.data_schema}_{self.symbol}"

    def redis_name(self):
        return f"{self.data_schema}:{self.vendor}:{self.symbol}"

    def file_name(self):
        pass


@dataclass
class Option1D:
    market: str
    date: str
    contract: str
    call_put: str
    strike: float
    settlement: float
    last: Optional[float] = None