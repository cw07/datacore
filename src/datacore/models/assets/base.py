import re
from zoneinfo import ZoneInfo
from pydantic import BaseModel, field_validator


class BaseAsset(BaseModel):
    dflow_id: str


class TradingHours(BaseModel):
    time_zone: str  # valid str values are: 'America/New_York'
    open_time_local: str # e.g. 'HH:MM:SS'
    close_time_local: str # e.g. 'HH:MM:SS'
    days: list[int] # list of integer from 0-6, maximum 7 days


    @field_validator("time_zone")
    @classmethod
    def validate_time_zone(cls, v: str) -> str:
        # Ensure it's a valid IANA time zone
        try:
            ZoneInfo(v)
        except Exception:
            raise ValueError(f"Invalid time zone: '{v}'. Must be a valid IANA zone like 'America/New_York'.")
        return v

    @field_validator("open_time_local", "close_time_local")
    @classmethod
    def validate_time_format(cls, v: str) -> str:
        # Must match HH:MM:SS (00-23):(00-59):(00-59)
        if not re.fullmatch(r"^(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d$", v):
            raise ValueError(f"Invalid time format: '{v}'. Expected 'HH:MM:SS' (24-hour).")
        return v

    @field_validator("days")
    @classmethod
    def validate_trading_days(cls, v: list[int]) -> list[int]:
        # Must contain integers between 0–6 (Monday–Sunday)
        if not all(isinstance(day, int) and 0 <= day <= 6 for day in v):
            raise ValueError("trading_days must contain integers from 0 to 6 (Mon–Sun).")
        if len(v) > 7:
            raise ValueError("trading_days can contain at most 7 days.")
        return v