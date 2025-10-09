import datetime as dt
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List, Literal

from .order import OrderSide, OrderAction


@dataclass
class OrderBookEvent:
    """
    Single order book event optimized for storage and reconstruction.
    """

    # Timestamps
    ts_recv: int          # Capture server received timestamp expressed as the number of nanoseconds since the UNIX epoch.
    ts_event: int         # Matching engine received timestamp expressed as the number of nanoseconds since the UNIX epoch.
    ts_in_delta: int      # The matching-engine-sending timestamp expressed as the number of nanoseconds before ts_recv.

    # Identifiers
    instrument_id: int    # Numeric instrument ID.
    symbol: str           # Requested symbol for the instrument.
    publisher_id: int     # Publisher ID assigned by Databento, which denotes dataset and venue.
    rtype: int            # Record type. Each schema corresponds with a single rtype value.
    sequence: int         # Message sequence number assigned at the venue.

    # Order details
    action: OrderAction   # Event action. Can be Add, Cancel, Modify, Clear book, or Trade.
    side: OrderSide       # Side that initiates the event. Can be Ask for the sell aggressor in a trade, Bid for the buy aggressor in a trade, or None where no side is specified by the original trade or the record was not a trade.
    price: int            # Order price expressed as a signed integer where every 1 unit corresponds to 1e-9.
    size: int             # Order quantity.

    # Metadata
    flags: int            # A bit field indicating event end, message characteristics, and data quality.
    channel_id: Optional[int] = None  # The channel ID assigned by Databento as an incrementing integer starting at zero.
    depth: Optional[int] = None  # Book level where the update event occurred.

    # Top-of-book state
    bid_px_00: Optional[float] = None  # Bid price at the top level.
    bid_sz_00: Optional[int] = None    # Bid size at the top level.
    bid_ct_00: Optional[int] = None    # Number of bid orders at the top level.
    ask_px_00: Optional[float] = None  # Ask price at the top level.
    ask_sz_00: Optional[int] = None    # Ask size at the top level.
    ask_ct_00: Optional[int] = None    # Number of ask orders at the top level.

    @property
    def ts_recv_dt(self) -> dt.datetime:
        """Convert ts_recv to datetime"""
        return dt.datetime.fromtimestamp(self.ts_recv / 1e9)

    @property
    def ts_event_dt(self) -> dt.datetime:
        """Convert ts_event to datetime"""
        return dt.datetime.fromtimestamp(self.ts_event / 1e9)

    @property
    def price_decimal(self) -> float:
        """Convert nano price to decimal"""
        return self.price / 1e9

    @property
    def is_trade(self) -> bool:
        """Check if this is a trade event"""
        return self.action in [OrderAction.TRADE, OrderAction.FILL]

    @property
    def is_book_update(self) -> bool:
        """Check if this is a book update event"""
        return self.action in [OrderAction.ADD, OrderAction.CANCEL, OrderAction.MODIFY]
