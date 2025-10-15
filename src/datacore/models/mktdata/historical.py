from typing import Optional

from dataclasses import dataclass,fields, asdict
from datacore.models.mktdata.base import BaseMarketData
from datacore.models.mktdata.schema import MktDataSchema

@dataclass
class OHLCV1D(BaseMarketData):
    open: float
    high: float
    low: float
    close: float
    ts_event: int # Matching engine received timestamp expressed as the number of nanoseconds since the UNIX epoch.
    volume: Optional[float] = None
    rtype: Optional[int] = None  # Record type. Each schema corresponds with a single rtype value.
    instrument_id: Optional[int] = None  # Numeric instrument ID.
    publisher_id: Optional[int] = None  # Publisher ID assigned by Databento, which denotes dataset and venue.

    data_schema = MktDataSchema.OHLCV_1D

    def from_dict(self, message: dict):
        pass

    def db_table_name(self):
        pass

    def redis_name(self):
        pass

    def file_name(self):
        pass