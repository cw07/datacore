from enum import StrEnum

class MktDataSchema(StrEnum):
    MBO = "mbo"
    MBP_1 = "mbp_1"
    MBP_10 = "mbp_10"
    TRADES = "trades"
    """
    Aggregate bars (OHLCV) provide open, high, low, and close prices and total volume
    aggregated from trades at 1-second, 1-minute, 1-hour, or 1-day intervals.
    """
    OHLCV_1S = "ohlcv_1s"
    OHLCV_1M = "ohlcv_1m"
    OHLCV_1H = "ohlcv_1h"
    OHLCV_1D = "ohlcv_1d"

    def short_name(self) -> str:
        """Return enum value with underscores removed"""
        return self.value.replace("_", "")
