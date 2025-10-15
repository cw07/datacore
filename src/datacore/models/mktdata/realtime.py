from enum import StrEnum
from typing import Optional
from dataclasses import dataclass, fields, asdict

from datacore.models.mktdata.base import BaseMarketData
from datacore.models.assets import AssetType
from datacore.models.order import OrderSide, OrderAction


class RealtimeSchema(StrEnum):
    MBO = "mbo"
    MBP_1 = "mbp_1"
    MBP_10 = "mbp_10"
    TRADES = "trades"
    """
    Aggregate bars (OHLCV) provide open, high, low, and close prices and total volume
    aggregated from trades at 1-second, 1-minute, 1-hour, or 1-day intervals.
    """
    OHLCV_1S = "ohlcv_1s"
    OHLCV_1M = "ohlcv_1m"
    OHLCV_1H = "ohlcv_1h"
    OHLCV_1D = "ohlcv_1d"

    def short_name(self) -> str:
        """Return enum value with underscores removed"""
        return self.value.replace("_", "")


@dataclass
class MarketByPrice1(BaseMarketData):
    symbol: str  # Requested symbol for the instrument.
    asset_type: AssetType
    price: int  # Order price expressed as a signed integer where every 1 unit corresponds to 1e-9.
    ts_recv: int  # Capture server received timestamp expressed as the number of nanoseconds since the UNIX epoch.
    vendor: str # Data vendor

    ts_event: Optional[int] = None  # Matching engine received timestamp expressed as the number of nanoseconds since the UNIX epoch.
    ts_in_delta: Optional[int] = None  # The matching-engine-sending timestamp expressed as the number of nanoseconds before ts_recv.

    # Order details
    action: Optional[OrderAction] = None  # Event action. Can be Add, Cancel, Modify, Clear book, or Trade.
    side: Optional[OrderSide] = None  # Side that initiates the event. Can be Ask for the sell aggressor in a trade, Bid for the buy aggressor in a trade, or None where no side is specified by the original trade or the record was not a trade.
    size: Optional[int] = None  # Order quantity.

    # Metadata
    instrument_id: Optional[int] = None  # Numeric instrument ID.
    publisher_id: Optional[int] = None  # Publisher ID assigned by Databento, which denotes dataset and venue.
    rtype: Optional[int] = None  # Record type. Each schema corresponds with a single rtype value.
    sequence: Optional[int] = None  # Message sequence number assigned at the venue.

    flags: Optional[int] = None  # A bit field indicating event end, message characteristics, and data quality.
    channel_id: Optional[int] = None  # The channel ID assigned by Databento as an incrementing integer starting at zero.
    depth: Optional[int] = None  # Book level where the update event occurred.
    db_schema: str = RealtimeSchema.MBP_1.short_name()

    # Top-of-book state
    bid_px_00: Optional[float] = None  # Bid price at the top level.
    bid_sz_00: Optional[int] = None  # Bid size at the top level.
    bid_ct_00: Optional[int] = None  # Number of bid orders at the top level.
    mid_px_00: Optional[float] = None # Mid price at the top level
    ask_px_00: Optional[float] = None  # Ask price at the top level.
    ask_sz_00: Optional[int] = None  # Ask size at the top level.
    ask_ct_00: Optional[int] = None  # Number of ask orders at the top level.

    @classmethod
    def from_dict(cls, message: dict):
        field_names = {f.name for f in fields(cls)}
        filtered_data = {k: v for k, v in message.items() if k in field_names}
        return cls(**filtered_data)

    def to_dict(self):
        return {k: v for k, v in asdict(self).items() if v is not None}

    def db_table_name(self):
        return f"{self.asset_type}_{self.symbol}_{self.db_schema}_{self.vendor}"

    def redis_name(self):
        return f"rt:onyx:{self.symbol}"

    def file_name(self):
        pass