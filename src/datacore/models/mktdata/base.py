from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict

from datacore.models.assets import AssetType


@dataclass
class BaseMarketData(ABC):
    asset_type: AssetType
    vendor: str
    symbol: str

    def from_dict(self, message: dict):
        pass

    def to_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None}

    @abstractmethod
    def db_table_name(self):
        pass

    @abstractmethod
    def redis_name(self):
        pass

    @abstractmethod
    def file_name(self):
        pass