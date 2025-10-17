from .tradingStratInterface import ITradingStrategy
from databaseInterface import IDatabase
import pandas as pd
import backtesting
class BuyAndHold(ITradingStrategy):
    
    def __init__(self, ibclient):
        
        self.client = ibclient
    
    def collectData(self, symbol, start, end, dbclient: IDatabase) -> pd.DataFrame:
        
        data = dbclient.getDailyCandleDataFromDB(symbol, start, end)
        return data
    

