from enum import StrEnum


class Frequency(StrEnum):
    """Data frequency types"""
    RAW = "raw"
    TICK = "tick"
    MIN_1 = "1min"
    MIN_5 = "5min"
    MIN_15 = "15min"
    HOUR_1 = "1hour"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
