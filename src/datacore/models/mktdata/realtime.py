from typing import Optional
from dataclasses import dataclass, fields, asdict

from datacore.models.mktdata.base import BaseMarketData
from datacore.models.order import OrderSide, OrderAction
from datacore.models.mktdata.schema import MktDataSchema


@dataclass
class MarketByPrice1(BaseMarketData):
    price: float
    ts_event: str  # Capture server received timestamp expressed as the number of nanoseconds since the UNIX epoch.

    ts_recv: Optional[int] = None  # Matching engine received timestamp expressed as the number of nanoseconds since the UNIX epoch.
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

    # Top-of-book state
    bid_px_00: Optional[float] = None  # Bid price at the top level.
    bid_sz_00: Optional[int] = None  # Bid size at the top level.
    bid_ct_00: Optional[int] = None  # Number of bid orders at the top level.
    mid_px_00: Optional[float] = None # Mid price at the top level
    ask_px_00: Optional[float] = None  # Ask price at the top level.
    ask_sz_00: Optional[int] = None  # Ask size at the top level.
    ask_ct_00: Optional[int] = None  # Number of ask orders at the top level.

    data_schema: str = MktDataSchema.MBP_1

    def to_dict(self):
        return {k: v for k, v in asdict(self).items() if v is not None}

    def db_table_name(self):
        return f"{self.asset_type}_{self.symbol}_{self.data_schema}_{self.vendor}"

    def redis_name(self):
        return f"rt:{self.vendor}:{self.symbol}"

    def file_name(self):
        pass