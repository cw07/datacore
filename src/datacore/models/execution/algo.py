from enum import StrEnum
from abc import ABC, abstractmethod


class BaseExecutionAlgo(ABC):
    """Abstract base class for execution algorithms, each platform may have its own implementation
    """

    @property
    @abstractmethod
    def short_name(self) -> str:
        pass

    @property
    @abstractmethod
    def duration(self) -> int:
        """Get duration in minutes for this algorithm type."""
        pass



class TimeInForce(StrEnum):
    DAY = "DAY"
    IOC = "IOC"  # Immediate or Cancel
    FOK = "FOK"  # Fill or Kill

    def __str__(self):
        return self.value


    def __repr__(self):
        return self.value