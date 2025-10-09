from enum import Enum
from abc import ABC, abstractmethod



class BaseSecurity(ABC):
    FX = "fx"
    FUT = "fut"
    EQUITY = "equity"
    EQUITY_OPTION = "equity_option"
    FUT_OPTION = "fut_option"

    @property
    @abstractmethod
    def is_fx(self):
        pass

    @property
    @abstractmethod
    def is_future(self):
        pass

    @property
    @abstractmethod
    def is_equity(self):
        pass

    @property
    @abstractmethod
    def is_equity_option(self):
        pass

    @property
    @abstractmethod
    def is_fut_option(self):
        pass

    @property
    @abstractmethod
    def is_option(self):
        pass


