import pytest
from src.dbento import DataBento
import pandas as pd



class TestDataBento():



    def test_getFuturesExpSymbols(self):
        
        pass

      

    def test_requestDailyFutureData(self):
        dbe = DataBento()

        data = pd.read_csv("dailyfuturedata.csv")

        dbe.backAdjustData(data)



