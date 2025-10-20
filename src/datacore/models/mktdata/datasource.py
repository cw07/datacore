from enum import StrEnum


class DataSource(StrEnum):
    """Data source types"""
    DataBento = "databento"
    BBG = "bbg"
    Onyx = "onyx"
    Sparta = "sparta"
    MarketDataDB = "mkt_db"
