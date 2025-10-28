from enum import StrEnum


class Venue(StrEnum):
    """Supported Venue types"""
    LME = "LME"
    CME = "CME"
    ICE = "ICE"
    GLOBAL = "GLOBAL"
    SGX = "SGX"
    ONYX = "ONYX"