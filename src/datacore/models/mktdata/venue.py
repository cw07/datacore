from enum import StrEnum


class Venue(StrEnum):
    """Supported Venue types"""
    LME = "lme"
    CME = "cme"
    ICE = "ice"
    GLOBAL = "global"
    SGX = "sgx"
    ONYX = "onyx"