import datetime as dt
from typing import Optional
from zoneinfo import ZoneInfo
from pydantic import BaseModel, Field, field_validator, computed_field, model_validator

from datacore.models.assets.base import BaseAsset, TradingHours
from datacore.models.mktdata.venue import Venue


class Forward(BaseAsset):
    contract_size: int
    venue: Venue
    hours: TradingHours

