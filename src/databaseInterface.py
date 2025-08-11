from abc import ABC, abstractmethod
import pandas as pd

class IDatabase(ABC):
   
    @abstractmethod
    def __init__(self, db_name:str):
        pass
    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self):
        pass

    @abstractmethod
    def init_db(self):
        pass

    @abstractmethod
    def _addSymbolsToDB(self):
        pass
    

    @abstractmethod
    def addCandleData(self, dataFrame: pd.DataFrame):
        pass

    @abstractmethod
    def getCandleData(self, start, end):
        pass
