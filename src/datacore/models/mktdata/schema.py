from enum import StrEnum

from datacore.models.mktdata.frequency import Frequency

class MktDataSchema(StrEnum):
    MBO = "mbo"
    MBP_1 = "mbp-1"
    MBP_10 = "mbp-10"
    TRADES = "trades"
    OHLCV_1S = "ohlcv-1s"
    OHLCV_1M = "ohlcv-1m"
    OHLCV_1H = "ohlcv-1h"
    OHLCV_1D = "ohlcv-1d"

    def short_name(self) -> str:
        """Return enum value with underscores removed"""
        return self.value.replace("_", "")

    @property
    def frequency(self):
        frequency_map = {
            MktDataSchema.MBO: Frequency.TICK,
            MktDataSchema.MBP_1: Frequency.TICK,
            MktDataSchema.MBP_10: Frequency.TICK,
            MktDataSchema.TRADES: Frequency.TICK,
            MktDataSchema.OHLCV_1S: Frequency.SEC_1,
            MktDataSchema.OHLCV_1M: Frequency.MIN_1,
            MktDataSchema.OHLCV_1H: Frequency.HOUR_1,
            MktDataSchema.OHLCV_1D: Frequency.DAY_1
        }
        return frequency_map[self]

