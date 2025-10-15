import datetime as dt
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
    ts_event: int
    volume: Optional[float] = None
    rtype: Optional[int] = None
    instrument_id: Optional[int] = None
    publisher_id: Optional[int] = None

    data_schema = MktDataSchema.OHLCV_1D

    @classmethod
    def from_dict(cls, message: dict):
        field_names = {f.name for f in fields(cls)}
        filtered_data = {k: v for k, v in message.items() if k in field_names}
        return cls(**filtered_data)

    def db_table_name(self):
        pass

    def redis_name(self):
        return f"{self.data_schema}:{self.vendor}:{dt.datetime.fromtimestamp(self.ts_event).strftime("%Y-%m-%d")}:{self.symbol}"

    def file_name(self):
        pass