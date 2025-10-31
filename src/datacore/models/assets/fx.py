from typing import Optional

from datacore.models.mktdata.venue import Venue
from datacore.models.assets.asset_type import AssetType
from datacore.models.mktdata.base import BaseMarketData
from datacore.models.assets.base import BaseAsset, TradingHours


class FXSpot(BaseAsset):
    hours: TradingHours
    venue: Venue
    symbol: Optional[str] = None
    description: str = ""
    asset_type: AssetType = AssetType.FX
    mkt_data: Optional[BaseMarketData] = None