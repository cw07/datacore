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

