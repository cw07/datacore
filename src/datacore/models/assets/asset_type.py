from enum import IntEnum, StrEnum


class AssetType(StrEnum):
    FX = "fx"
    FUT = "fut"
    FWD = "fwd"
    INDEX = "index"
    EQUITY = "equity"
    EQUITY_OPTION = "equityoption"
    FUT_OPTION = "futoption"

    def is_fx(self):
        pass

    def is_future(self):
        pass

    def is_equity(self):
        pass

    def is_equity_option(self):
        pass

    def is_fut_option(self):
        pass

    def is_option(self):
        pass


class OptionType(IntEnum):
    Call = 1
    Put = -1

    def __str__(self):
        return 'C' if self is OptionType.Call else 'P'

    def __repr__(self):
        return f"OptionType.{self.name}"

    @classmethod
    def from_str(cls, s: str) -> 'OptionType':
        """Create an OptionType from a string ('C' or 'P', case-insensitive)."""
        if not isinstance(s, str):
            raise TypeError(f"Expected str, got {type(s).__name__}")
        s_upper = s.upper()
        if s_upper == 'C':
            return cls.Call
        elif s_upper == 'P':
            return cls.Put
        else:
            raise ValueError(f"Invalid option type string: {s!r}. Expected 'C' or 'P'.")
