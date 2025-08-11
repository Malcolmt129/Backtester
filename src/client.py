import time
import pytz
import pandas as pd
from datetime import datetime
from .databaseInterface import IDatabase
from ibapi.client import BarData, EClient 
from ibapi.wrapper import EWrapper
from ibapi.client import Contract
from threading import Thread

class IBClient(EWrapper, EClient):
    
    def __init__(self, host, port, client_id, dbconn: IDatabase) -> None:

        EClient.__init__(self, self)
        self.connect(host, port, client_id)
        self.data = {}

        self.dbconn = dbconn 

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
        print(f"ERR  {errorCode}: {errorString}")
        # if there’s extra data, dump it
        if args:
            print(" Extra error info:", args)
    

    def _datarequest(self, reqId: int, contract: Contract,
                              end:str="", durationStr: str="1 D", barSizeSetting: str= "1 min",
                              useRTH:int=0, formatDate:int=2, 
                              keepUpToDate:bool=False) -> pd.DataFrame:
        try:
            self.reqHistoricalData(reqId=reqId,
                                contract=contract,
                                endDateTime=end,
                                durationStr=durationStr,
                                barSizeSetting=barSizeSetting,
                                whatToShow="TRADES",
                                useRTH=useRTH,
                                formatDate=formatDate,
                                keepUpToDate=keepUpToDate,
                                chartOptions=[])
            
            time.sleep(3) # IB takes some time to process requests... need this
            return self.data[reqId]

        except KeyError  as e:
            print(f"Error: {e}, granularity is too small for duration period") 

            return pd.DataFrame(columns=["date", "open", "high", "low", "close"]).set_index("date")


    #Historical data is some type of callback and you cant change the name or you will get nothing
    #back
    def historicalData(self, reqId: int, bar: BarData) -> None:
        df = self.data.setdefault(reqId, 
                                  pd.DataFrame(columns=["date", "open", "high", "low", "close",
                                                        "volume"]).set_index("date"))
        
        dateString = str(bar.date)
        

        try: 
            dt_object = datetime.strptime(dateString, "%Y%m%d") 
            
            localizedTime = self._localizeTime_large_gran(dt_object)
            df.loc[localizedTime] = [bar.open, bar.high, bar.low, bar.close, bar.volume]
        
        except ValueError:
            localizedTime = self._localizeTime(dateString)
            df.loc[localizedTime] = [bar.open, bar.high, bar.low, bar.close, bar.volume]


    def _localizeTime(self, timeStamp: str):
        tz = pytz.timezone('America/New_York')
        # directly get a TZ-aware datetime in New York
        dt = tz.localize(datetime.fromtimestamp(int(timeStamp)))
        return dt
    
    def _localizeTime_large_gran(self, timeStamp: datetime):

        tz = pytz.timezone('America/New_York')
        
        dt = tz.localize(timeStamp)
        return dt


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
    
    
    # Remember that this is just a request to get something back. So the member variables that you
    # see are not the only attributes of the contracts return object
    @staticmethod
    def get_futures_contract(symbol: str, localsymbol: str = "", expiry: str = ""):
        contract = Contract()
        contract.symbol = symbol
        contract.secType = "CONTFUT"
        contract.exchange = "CME"
        contract.localSymbol = localsymbol
        contract.currency = "USD"
        contract.lastTradeDateOrContractMonth = expiry
        contract.includeExpired = True 
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
