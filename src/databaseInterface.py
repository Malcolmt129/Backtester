from abc import ABC, abstractmethod
import pandas as pd

class IDatabase(ABC):
   
    @abstractmethod
    def __init__(self, db_name:str):
        pass

    @abstractmethod
    def __exit__(self):
        pass

    @abstractmethod
    def init_db(self):
        pass

    @abstractmethod
    def addDailyCandleData(self, contract: str, historicalData: pd.DataFrame):
        pass

    @abstractmethod
    def getDailyCandleDataFromDB(self,symbol: str, start: str, end: str) -> pd.DataFrame:
        pass
