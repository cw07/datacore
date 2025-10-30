import datetime as dt
from typing import Optional

from datacore.models.mktdata.venue import Venue
from datacore.models.assets.asset_type import AssetType
from datacore.models.mktdata.base import BaseMarketData
from datacore.models.assets.base import BaseAsset, TradingHours


class Forward(BaseAsset):
    contract_size: int
    venue: Venue
    expiry: dt.date
    hours: TradingHours
    symbol: Optional[str] = None
    asset_type: AssetType = AssetType.FWD
    mkt_data: Optional[BaseMarketData] = None

