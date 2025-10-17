from abc import ABC, abstractmethod
from databaseInterface import IDatabase
import pandas as pd

class ITradingStrategy(ABC):
    

    @abstractmethod
    def __init__(self, ibclient):
        pass

    
    @abstractmethod
    def collectData(self, symbol, start, end, dbclient: IDatabase) -> pd.DataFrame:
        pass

