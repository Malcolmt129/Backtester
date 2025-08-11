from abc import ABC, abstractmethod


class ITradingStrategy(ABC):
    

    @abstractmethod
    def __init__(self, ibclient):
        pass


    @abstractmethod
    def collectData(self):
        pass


    @abstractmethod
    def generateSignals(self):
        pass






