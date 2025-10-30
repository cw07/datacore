import datetime as dt
from typing import Optional
from zoneinfo import ZoneInfo
from pydantic import BaseModel, Field, field_validator, computed_field, model_validator

from datacore.models.assets.asset_type import AssetType, OptionType
from datacore.models.mktdata.venue import Venue
from datacore.utils.common import CONTRACT_MONTH_CODE


class BaseFutures(BaseModel):
    dflow_id: str
    terms: int
    contract_size: int
    venue: Venue
    time_zone: str
    open_time_local: str
    close_time_local: str
    trading_days: list[int]
    contract_months: list[str]
    description: Optional[str] = None
    category: Optional[str] = None

    @computed_field
    @property
    def contract_month_code(self) -> list[str]:
        return [CONTRACT_MONTH_CODE[m] for m in self.contract_months]

    @computed_field
    @property
    def tz(self) -> ZoneInfo:
        return ZoneInfo(self.time_zone)

    @computed_field
    @property
    def is_overnight(self) -> bool:
        is_overnight = self.open_time_local > self.close_time_local
        return is_overnight

    def is_trading_now(self) -> bool:
        """
        Returns True if the market is currently trading.
        Uses string comparison to detect overnight sessions (e.g. '18:00:00' > '17:00:00').
        """
        now_local = dt.datetime.now(self.tz)
        now_local_weekday = now_local.weekday()
        now_local_time_str = now_local.strftime("%H:%M:%S")

        if not self.is_overnight:
            if now_local_weekday not in self.trading_days:
                return False
            return self.open_time_local <= now_local_time_str < self.close_time_local
        else:
            if self.open_time_local <= now_local_time_str:
                # Session started today (e.g. 18:00–23:59)
                session_start_weekday = now_local_weekday
            elif now_local_time_str < self.close_time_local:
                # Session started yesterday (e.g. 00:00–17:00)
                session_start_weekday = (now_local - dt.timedelta(days=1)).weekday()
            else:
                # Time is in the gap: close_time <= now < open_time → market closed
                return False

            return session_start_weekday in self.trading_days

    @property
    def trading_session(self) -> str | None:
        if not self.is_trading_now():
            return None

        now_local = dt.datetime.now(self.tz)
        now_local_time_str = now_local.strftime("%H:%M:%S")

        if not self.overnight:
            session_date = now_local.date()
        else:
            if now_local_time_str >= self.open_time_local:
                session_date = now_local.date()
            else:
                session_date = (now_local - dt.timedelta(days=1)).date()

        return session_date.strftime("%Y-%m-%d")


class Futures(BaseModel):
    dflow_id: str
    parent: BaseFutures
    venue: Optional[Venue] = None
    description: Optional[str] = None
    symbol: Optional[str] = None
    asset_type: AssetType = AssetType.FUT

    @model_validator(mode="after")
    def set_venue_from_parent(self) -> 'Futures':
        if self.venue is None:
            self.venue = self.parent.venue
        return self

    def is_trading_now(self) -> bool:
        return self.parent.is_trading_now()

    @property
    def trading_session(self) -> str | None:
        return self.parent.trading_session


class FuturesOptions(BaseModel):
    dflow_id: str
    parent: Futures
    call_put: OptionType
    strike: float
    expiry: dt.date
    venue: Optional[Venue] = None
    description: Optional[str] = None
    asset_type: AssetType = AssetType.FUT_OPTION

    @model_validator(mode="after")
    def set_venue_from_parent(self) -> 'FuturesOptions':
        if self.venue is None:
            self.venue = self.parent.venue
        return self

    def is_trading_now(self) -> bool:
        return self.parent.is_trading_now()

    @property
    def trading_session(self) -> str | None:
        return self.parent.trading_session



if __name__ == "__main__":
    cme_cl = BaseFutures(dflow_id="CME.CL",
                         terms=12,
                         contract_size=1000,
                         venue=Venue.CME,
                         time_zone="America/New_York",
                         open_time_local="18:00:00",
                         close_time_local="17:00:00",
                         trading_days=[6,0,1,2,3,4],
                         contract_months=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                         )

    cme_cl_1 = Futures(dflow_id="CME.CL.1",
                       parent=cme_cl,
                       description="CME CL 1"
                       )

    cme_cl_1_opt = FuturesOptions(dflow_id="12",
                                  parent=cme_cl_1,
                                  description="CME CL 1",
                                  call_put=OptionType.Call,
                                  strike=1000,
                                  expiry=dt.date.today(),
                                  )

    print(cme_cl_1_opt)


