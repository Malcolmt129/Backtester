
from abc import ABC, abstractmethod

from backtester.tradingEngine import TradingEngine


class IView():

    @abstractmethod 
    def build(self):
        pass

    
