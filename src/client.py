import time
from ibapi import client
import pytz
import pandas as pd
from datetime import datetime, date, timedelta
from databaseInterface import IDatabase
from ibapi.client import BarData, EClient 
from ibapi.wrapper import EWrapper
from ibapi.client import Contract
from threading import Thread, Event
import pdb
import logging 


log = logging.getLogger(__name__)
#logging.basicConfig(level=logging.DEBUG)


class IBClient(EWrapper, EClient):
    
    def __init__(self, host, port, client_id, dbconn: IDatabase) -> None:

        EClient.__init__(self, self)
        self.connected = False
        self.lastLookedContract = None
        self.dbconn = dbconn 
        
        
        #To do: Make a config file for this...
        self.host = host
        self.port = port
        self.clientId = client_id

        self.connectIB(host, port, client_id)

        self.data = {} 
        self.done = Event()

        self.thread = None
        self.shutdown_flag = Event()



    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
    


    def connectIB(self, host, port, client_id):
        
        """
            This wrapper method creates the thread that connects to TWS
        """
        
        def connect_thread(): 
            """
                The structure of this connect is based on combating the hanging thread that happens
                often during troubleshooting and potentially while running, where the thread isn't
                terminated gracefully. self.shutdown_flag is an Event object that we can use to
                communicate what is going on with other threads, so while not set, go ahead and run.
                When set (which will only happen if error 326 occurs), that means kill the thread and do
                some clean up. 

            """
            try:
                self.connect(host,port,client_id)

                while not self.shutdown_flag.is_set():
                    self.run()

            except Exception as e:
                log.error(f"Connection error {e}")

        thread = Thread(target=connect_thread, daemon=True)
        thread.start()
        
    

    def wait_until_connected(self, timeout=10):

        """
            This is neccessary because requesting data before the connection is establish will cause a
            hard to detect error (unless logging is on, which I wont have on when things start to work
            well together)
        """
        for _ in range(timeout * 10):
            if self.connected:
                return True
            time.sleep(0.1)

        raise TimeoutError("Timeout waiting for TWS to connect")

    
    def nextValidId(self, orderId: int):
        """
        Per the TWS api docs, this function (which is an override of EWrapper or EClient class
        (don't care to look which one right now) is commonly used to tell if TWS is connected or
        not.
        """
        self.connected = True
        log.info("Connection to TWS established")


    def cleanup(self):
        """ 
            This is what will be called when we get error code 326.
        """

        self.shutdown_flag.set()
        self.disconnect()
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2)
            log.info("Thread successfully shut down.")


    def reconnect(self):
        """ 
            This is what will be called when we get error code 326.
        """
        time.sleep(2)


        #clear flags
        self.connected = False
        self.shutdown_flag.clear()
        self.done.clear()

        
        #Restart thread
        self.connectIB(self.host, self.port, self.clientId )


    def error(self, *args, **kwargs):
        # Parse based on known formats
        if len(args) == 3:
            req_id, code, msg = args
        elif len(args) == 4:
            req_id, code, msg, extra = args
        else:
            print("Unknown error format:", args)
            return

        # General log
        print(f"⚠️  IB Error {code}: {msg} (req_id={req_id})")

        # Route based on error code
        if code == 200:
            print("🔴 No security definition found (possibly bad symbol or contract).")
        elif code == 326:
            print("🔴 Client ID in use already... closing connection and retrying.")
            
            self.cleanup()
            self.reconnect()

        elif code == 504:
            print("🔴 TWS not connected.")
        elif code == 1101:
            print("🟡 TWS connection restored.")
        elif code == 202:
            print("🟠 Order canceled.")
        elif code == 10147:
            print("🔵 Order rejected by exchange. You may want to retry.")
        else:
            print("ℹ️  Unhandled error code.")

        # Optional: raise custom exceptions
        if code in {200, 1100, 10147}:
            raise RuntimeError(f"TWS Critical Error [{code}]: {msg}")
    
    def dailyDataRequest(self, symbol: str, yearsback: int):

        """
        Retrieves daily candlestick data for specific futures contracts (quarterly expiries) over N years.
        """
        all_data = []
        expiries = self._get_past_expiries(yearsback)
        
        log.info("expiries have been set") 

        self.wait_until_connected()

        for i, expiry in enumerate(expiries):
            self.data[1] = []  # clear previous contract data
            self.done.clear()
            
            contract = self._get_futures_contract(symbol, expiry=expiry)
            print(contract)
            log.info(f"📦 Requesting {contract.symbol} for expiry {expiry}")

            try:
                super().reqHistoricalData(
                    reqId=1,
                    contract=contract,
                    endDateTime="",
                    durationStr="6 M", 
                    barSizeSetting="1 day",
                    whatToShow="TRADES",
                    useRTH=0,
                    formatDate=2,
                    keepUpToDate=False,
                    chartOptions=[]
                )

                self.done.wait(timeout=15)

                if self.data[1]:
                    df = pd.DataFrame(self.data[1])
                    df["expiry"] = expiry  # add expiry tag
                    all_data.append(df)
                else:
                    log.info(f"No data returned for {contract.symbol} expiry {expiry}")

            except Exception as e:
                print(f"Error requesting data for expiry {expiry}: {e}")

            time.sleep(0.5)  # slight buffer to avoid pacing violations

        if all_data:
            result = pd.concat(all_data).drop_duplicates(subset="date").sort_values("date")
            return result.reset_index(drop=True)
        else:
            log.warning("No data collected.")
            return pd.DataFrame()


    def _get_past_expiries(self, years=10):
        """
            Get the most liquid expiries strings to place as contract end dates for reqHistoricalData()
            function.
        """
        expiries = []
        today = datetime.today()
        current_year = today.year
        months = ["03", "06", "09", "12"]

        for y in range(current_year - years, current_year + 1):
            for m in months:
                expiries.append(f"{y}{m}")
        return expiries


   #Historical data is a EWrapper class function. This is called after you request data. You get
    #bar data back and you should put into a Dataframe to be able to manipulate later
    

    def historicalData(self, reqId: int, bar: BarData):
        
        if 1 not in self.data:
            self.data[reqId] = []
        
        # TO DO: Differentiate between the smaller and larger granularity formatting
        self.data[reqId].append({
            "date": self._localizeTime_Ymmdd(bar.date),
            "open": bar.open,
            "high": bar.high,
            "low": bar.low,
            "close": bar.close,
            "volume": int(bar.volume),
            })

    
    def historicalDataEnd(self, reqId: int, start: str, end: str):
        self.done.set()
        print(f"Historical data has been recieved for reqID {reqId}")


    def getLastLookedContract(self):
      return self.lastLookedContract


    def _localizeTime(self, timeStamp: str):
        tz = pytz.timezone('America/New_York')
        # directly get a TZ-aware datetime in New York
        dt = tz.localize(datetime.fromtimestamp(int(timeStamp)))
        return dt
    
    def _localizeTime_Ymmdd(self, timeStamp: str):
        
        tz = pytz.timezone('America/New_York')
        dt = datetime.strptime(timeStamp, "%Y%m%d").replace(tzinfo=tz)
        epoch_time = dt.timestamp() 
        return epoch_time 
    
    def _createDateObjFromString(self, input: str):
        return date.fromisoformat(input)

    def _get_stock_contract(self, symbol: str):
        contract = Contract()
        contract.symbol = symbol
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"

        self.lastLookedContract = contract.symbol

        return contract
    
    def _get_forex_contract(self, symbol: str):
        contract = Contract()
        contract.symbol = symbol
        contract.secType = "CASH"
        contract.exchange = "SMART"
        contract.currency = "USD"
        
        self.lastLookedContract = contract.symbol
       
        return contract
    

    
    # Remember that this is just a request to get something back. So the member variables that you
    # see are not the only attributes of the contracts return object
    def _get_futures_contract(self, symbol: str, localsymbol: str = "", expiry: str = ""):
        contract = Contract()
        contract.symbol = symbol
        contract.secType = "FUT"
        contract.exchange = "CME"
        contract.localSymbol = localsymbol
        contract.currency = "USD"
        contract.lastTradeDateOrContractMonth = expiry
        contract.includeExpired = True 

        self.lastLookedContract = contract.symbol
        
        return contract
    
    def _get_options_contract(self, symbol: str):
        contract = Contract()
        contract.symbol = symbol
        contract.secType = "OPT"
        contract.exchange = "SMART"
        contract.currency = "USD"

        self.lastLookedContract = contract.symbol

        return contract


if __name__ == "__main__":
    pass
