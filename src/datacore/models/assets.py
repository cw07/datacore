from enum import StrEnum


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


