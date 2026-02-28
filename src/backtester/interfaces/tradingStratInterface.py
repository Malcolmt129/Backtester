from abc import ABC, abstractmethod
from backtester.interfaces.databaseInterface import IDatabase
import pandas as pd

class ITradingStrategy(ABC):
    

    @abstractmethod
    def __init__(self, ibclient):
        pass

    @abstractmethod
    def start(self):
        pass
    
    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def on_event(self, event):
        pass


