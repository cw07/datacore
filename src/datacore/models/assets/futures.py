import datetime as dt
from typing import Optional
from zoneinfo import ZoneInfo
from pydantic import BaseModel, Field, field_validator, computed_field, model_validator

from datacore.models.mktdata.venue import Venue
from datacore.utils.common import CONTRACT_MONTH_CODE
from datacore.models.mktdata.base import BaseMarketData
from datacore.models.assets.base import BaseAsset, TradingHours
from datacore.models.assets.asset_type import AssetType, OptionType


class BaseFutures(BaseAsset):
    terms: int
    contract_size: int
    venue: Venue
    hours: TradingHours
    contract_months: list[str]
    description: str = ""
    category: Optional[str] = None

    @computed_field
    @property
    def contract_month_code(self) -> list[str]:
        return [CONTRACT_MONTH_CODE[m] for m in self.contract_months]

    @computed_field
    @property
    def is_overnight(self) -> bool:
        is_overnight = self.hours.open_time_local[0] > self.hours.close_time_local[-1]
        return is_overnight

class Futures(BaseAsset):
    parent: BaseFutures
    term: int
    expiry: Optional[dt.date] = None
    symbol: Optional[str] = None
    description: str = ""
    asset_type: AssetType = AssetType.FUT
    mkt_data: Optional[BaseMarketData] = None

    @property
    def venue(self) -> Venue:
        return self.parent.venue

    @property
    def contract_size(self):
        return self.parent.contract_size

    @property
    def hours(self) -> TradingHours:
        return self.parent.hours

    @property
    def category(self) -> str:
        return self.parent.category

    @property
    def trading_session(self) -> dt.date:
        return self.parent.trading_session

    @property
    def is_open(self) -> bool:
        return self.parent.is_open

    @model_validator(mode='after')
    def resolve_description(self) -> 'Futures':
        term_in_word = {1: "1st", 2: "2nd", 3: "3rd"}
        self.description = term_in_word.get(self.term, str(self.term) + "th") + " " + self.parent.description
        return self


class FuturesOptions(BaseAsset):
    parent: Futures
    term: int
    description: str = ""
    asset_type: AssetType = AssetType.FUT_OPTION
    mkt_data: Optional[BaseMarketData] = None

    @property
    def venue(self) -> Venue:
        return self.parent.venue

    @property
    def contract_size(self):
        return self.parent.contract_size

    @property
    def trading_session(self) -> dt.date:
        return self.parent.trading_session

    @property
    def is_open(self) -> bool:
        return self.parent.is_open

    @model_validator(mode='after')
    def resolve_description(self) -> 'FuturesOptions':
        self.description = self.parent.description + " Options"
        return self


if __name__ == "__main__":
    cme_cl = BaseFutures(dflow_id="CME.CL",
                         terms=12,
                         contract_size=1000,
                         venue=Venue.CME,
                         hours=TradingHours(time_zone="America/New_York",
                                            open_time_local=["18:00:00"],
                                            close_time_local=["17:00:00"],
                                            days=[6, 0, 1, 2, 3, 4]
                                            ),
                         contract_months=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                         )

    cme_cl_1 = Futures(dflow_id="CME.CL.1",
                       parent=cme_cl,
                       term=1,
                       description="CME CL 1"
                       )

    cme_cl_1_opt = FuturesOptions(dflow_id="12",
                                  parent=cme_cl_1,
                                  description="CME CL 1",
                                  term=1
                                  )

    print(cme_cl_1_opt.is_open)
    print(cme_cl_1_opt)


