from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict, fields

from datacore.models.assets import AssetType


@dataclass
class BaseMarketData(ABC):
    asset_type: AssetType
    vendor: str
    symbol: str

    @classmethod
    def from_dict(cls, message: dict):
        field_names = {f.name for f in fields(cls)}
        filtered_data = {k: v for k, v in message.items() if k in field_names}
        return cls(**filtered_data)

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

    def __repr__(self):
        field_strs = []
        for f in fields(self):
            value = getattr(self, f.name)
            field_strs.append(f"{f.name}={value!r}")
        return f"{self.__class__.__name__}({', '.join(field_strs)})"