from abc import ABC, abstractmethod


class BaseMarketData(ABC):

    @abstractmethod
    def db_table_name(self):
        pass

    @abstractmethod
    def redis_name(self):
        pass

    @abstractmethod
    def file_name(self):
        pass