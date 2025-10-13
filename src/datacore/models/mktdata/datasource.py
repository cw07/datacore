from enum import StrEnum


class DataSource(StrEnum):
    """Data source types"""
    DataBento = "databento"
    BBG = "bbg"
    InfluxDB = "influx"
    Sparta = "sparta"
