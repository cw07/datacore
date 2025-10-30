from enum import StrEnum


class Venue(StrEnum):
    """Supported Venue types"""
    LME = "LME"
    CME = "CME"
    ICE = "ICE"
    GLOBAL = "GLOBAL"
    SGX = "SGX"
    ONYX = "ONYX"

    def ccy(self) -> str:
        """Return the default quote currency for the venue"""
        mapping = {
            "LME": "USD",
            "CME": "USD",
            "ICE": "USD",
            "GLOBAL": "USD",
            "SGX": "USD",  # most SGX contracts are USD, some may be SGD depending on contract
            "ONYX": "USD",  # placeholder, depends on your internal setup
        }
        return mapping[str(self.value)]
