from client import IBClient
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf
from .databaseInterface import IDatabase

class DailyStdDev():



    def __init__(self, ibclient: IBClient):
        
        self.client = ibclient


    def collectData(self, symbol: str, end: str= ""):

            contract = self.client.get_futures_contract(symbol)
            data = self.client._datarequest(99, contract, end=end, durationStr="5 Y",
                                                     barSizeSetting= "1 Day")
            return data


if __name__ == "__main__":
    pass        

