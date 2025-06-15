import time
import pytz
from typing import Dict, Optional
import pandas as pd
from datetime import datetime

from ibapi.client import BarData, EClient 
from ibapi.wrapper import EWrapper
from ibapi.client import Contract
from threading import Thread

class IBClient(EWrapper, EClient):
    
    def __init__(self, host, port, client_id) -> None:

        EClient.__init__(self, self)
        self.connect(host, port, client_id)
        self.data: Dict[int, pd.DataFrame] = {}


        thread = Thread(target=self.run, daemon=True)
        thread.start()

    def __enter__(self):
        return self

    def __exit__(self,  exc_type, exc, tb):
        return self.disconnect()

   # catch _any_ variant of error()
    def error(self, reqId=None, errorCode=None, errorString=None, *args):
        """
        This will handle:
          - error(id, code, msg)
          - error(id, code, msg, advancedOrderRejectJson)
          - and any future variants without raising a signature error
        """
        # basic info
        print(f"ERR  {errorCode}: {errorString}")
        # if there’s extra data, dump it
        if args:
            print(" Extra error info:", args)
    

    def requestHistoricalData(self, reqId: int, contract: Contract) -> pd.DataFrame:

        self.data[reqId] = pd.DataFrame(columns=["time", "open", "high", "low", "close"])
        self.data[reqId].set_index("time", inplace=True)


        self.reqHistoricalData(reqId=reqId,
                               contract=contract,
                               endDateTime="",
                               durationStr="1 D",
                               barSizeSetting="1 min",
                               whatToShow="MIDPOINT",
                               useRTH=0,
                               formatDate=2,
                               keepUpToDate=False,
                               chartOptions=[])
        
        time.sleep(3) # IB takes some time to process requests... need this
        return self.data[reqId]
    
    #Historical data is some type of callback and you cant change the name or you will get nothing
    #back
    def historicalData(self, reqId: int, bar: BarData) -> None:
        df = self.data[reqId]
        df.loc[
                self.localizeTime(bar.date),
                ["open", "high", "low", "close"]
              ] = [bar.open, bar.high, bar.low, bar.close]
        df = df.astype(float)
        self.data[reqId] = df

    def localizeTime(self, timeStamp: str):
        tz = pytz.timezone('America/New_York')
        # directly get a TZ-aware datetime in New York
        dt = datetime.fromtimestamp(int(timeStamp), tz)
        return dt.strftime('%Y-%m-%d %H:%M:%S')


    @staticmethod 
    def get_stock_contract(symbol: str):
        contract = Contract()
        contract.symbol = symbol
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"
        return contract
    
    @staticmethod
    def get_forex_contract(symbol: str):
        contract = Contract()
        contract.symbol = symbol
        contract.secType = "CASH"
        contract.exchange = "SMART"
        contract.currency = "USD"
        return contract
    

    @staticmethod
    def get_futures_contract(symbol: str, localsymbol: str = "", expiry: str = ""):
        contract = Contract()
        contract.symbol = symbol
        contract.secType = "FUT"
        contract.exchange = "SMART"
        contract.localSymbol = localsymbol
        contract.currency = "USD"
        contract.lastTradeDateOrContractMonth = expiry
        return contract
    
    @staticmethod
    def get_options_contract(symbol: str):
        contract = Contract()
        contract.symbol = symbol
        contract.secType = "OPT"
        contract.exchange = "SMART"
        contract.currency = "USD"
        return contract

if __name__ == "__main__":
    pass
