from enum import StrEnum


class DataOutput(StrEnum):
    database = "database"
    redis = "redis"
    file = "file"