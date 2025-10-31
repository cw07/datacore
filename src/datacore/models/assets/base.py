import re
from zoneinfo import ZoneInfo
from pydantic import BaseModel, field_validator, model_validator


class BaseAsset(BaseModel):
    dflow_id: str


class TradingHours(BaseModel):
    time_zone: str  # valid str values are: 'America/New_York'
    open_time_local: list[str]   # 'HH:MM:SS'
    close_time_local: list[str]  # 'HH:MM:SS'
    days: list[int] # days open, list of integer from 0-6, maximum 7 days

    @field_validator("open_time_local", "close_time_local")
    @classmethod
    def validate_time_format(cls, v: list[str]) -> list[str]:
        """Validate each time string in the list matches HH:MM:SS format (24-hour)."""
        pattern = r"^(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d$"
        for time_str in v:
            if not isinstance(time_str, str):
                raise ValueError(f"Time must be a string, got {type(time_str).__name__}: {time_str}")
            if not re.fullmatch(pattern, time_str):
                raise ValueError(f"Invalid time format: '{time_str}'. Expected 'HH:MM:SS' (24-hour).")
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

    @model_validator(mode='after')
    def validate_open_close_length_match(self):
        """Ensure open_time_local and close_time_local have the same length."""
        if len(self.open_time_local) != len(self.close_time_local):
            raise ValueError(
                f"open_time_local and close_time_local must have the same length. "
                f"Got {len(self.open_time_local)} open times and {len(self.close_time_local)} close times."
            )
        return self

