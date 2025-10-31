import datetime as dt
from typing import Optional
from zoneinfo import ZoneInfo
from pydantic import computed_field

from datacore.models.mktdata.venue import Venue
from datacore.models.assets.asset_type import AssetType
from datacore.models.mktdata.base import BaseMarketData
from datacore.models.assets.base import BaseAsset, TradingHours


class Index(BaseAsset):
    venue: Venue
    hours: TradingHours
    symbol: Optional[str] = None
    description: str = ""
    asset_type: AssetType = AssetType.INDEX
    mkt_data: Optional[BaseMarketData] = None

    @computed_field
    @property
    def tz(self) -> ZoneInfo:
        return ZoneInfo(self.hours.time_zone)


    @property
    def is_open(self) -> bool:
        """
        Returns True if the market is currently trading.
        Uses string comparison to detect overnight sessions (e.g. '18:00:00' > '17:00:00').
        """
        now_local = dt.datetime.now(self.tz)
        now_local_weekday = now_local.weekday()
        now_local_time_str = now_local.strftime("%H:%M:%S")
