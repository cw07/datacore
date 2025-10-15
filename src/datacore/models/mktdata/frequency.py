from enum import StrEnum


class Frequency(StrEnum):
    """Data frequency types"""
    RAW = "raw"
    TICK = "tick"
    SEC_1 = "1sec"
    MIN_1 = "1min"
    MIN_5 = "5min"
    MIN_15 = "15min"
    HOUR_1 = "1hour"
    DAY_1 = "1day"
    WEEK_1 = "1week"
    MONTH_1 = "1month"
