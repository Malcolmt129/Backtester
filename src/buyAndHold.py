from .tradingStratInterface import ITradingStrategy
from .



class BuyAndHold(ITradingStrategy):
    
    def __init__(self, ibclient):
        
        self.client = ibclient
    
    def collectData(self):
         

