from typing import assert_type
from client import IBClient
import pandas as pd
import pytest


class TestIBClient:


    def test_historical_data_retrieval(self):
        client = IBClient("127.0.0.1", 7497, 5)
        mnq = client.get_futures_contract('mnq')
        data_mnq = client.requestHistoricalData(90, mnq, durationStr= "1 D", barSizeSetting="5 mins")
        
        assert_type(data_mnq, pd.DataFrame)
        
        assert_type(data_mnq.iloc[:, 0], str)
        assert_type(data_mnq.iloc[:, 1], float)
    
    def test_acquire_futures_contracts(self):
        client = IBClient("127.0.0.1", 7497, 5)
        client.



