import re
import datetime as dt
from zoneinfo import ZoneInfo
from pydantic import BaseModel, field_validator, model_validator, computed_field


class BaseAsset(BaseModel):
    dflow_id: str

    @property
    def is_open(self) -> bool:
        return self.hours.is_open

    @property
    def trading_session(self) -> dt.date:
        return self.hours.trading_session


class TradingHours(BaseModel):
    time_zone: str  # valid str values are: 'America/New_York'
    open_time_local: list[str]   # 'HH:MM:SS'
    close_time_local: list[str]  # 'HH:MM:SS'
    days: list[int] # days open, list of integer from 0-6, maximum 7 days

    @field_validator("open_time_local", "close_time_local")
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

    @computed_field
    @property
    def tz(self) -> ZoneInfo:
        return ZoneInfo(self.time_zone)

    @property
    def is_open(self) -> bool:
        """
        Returns True if the market is currently trading.
        Uses string comparison to detect overnight sessions (e.g. '18:00:00' > '17:00:00').
        """
        now_local = dt.datetime.now(self.tz)
        open_time = dt.datetime.strptime(self.open_time_local[0], "%H:%M:%S").time()
        trading_date = self.trading_session

        for open_t, close_t in zip(self.open_time_local, self.close_time_local):
            open_dt = dt.datetime.strptime(open_t, "%H:%M:%S").time()
            close_dt = dt.datetime.strptime(close_t, "%H:%M:%S").time()

            if close_dt < open_time:
                close_date = trading_date + dt.timedelta(days=1)
            else:
                close_date = trading_date
            close_full = dt.datetime.combine(close_date, close_dt).replace(tzinfo=self.tz)

            if open_dt < open_time:
                open_date = trading_date + dt.timedelta(days=1)
            else:
                open_date = trading_date
            open_full = dt.datetime.combine(open_date, open_dt).replace(tzinfo=self.tz)

            if open_full < now_local < close_full:
                return True
        return False

    @property
    def trading_session(self) -> dt.date:
        now = dt.datetime.now(self.tz)
        now_hms = now.strftime("%H:%M:%S")
        now_date = now.date()
        first_open_time = self.open_time_local[0]
        if now_hms < first_open_time:
            session_date = now_date - dt.timedelta(days=1)
        else:
            session_date = now_date

        if session_date.weekday() not in self.days:
            while session_date.weekday() not in self.days:
                session_date = session_date - dt.timedelta(days=1)
        return session_date

