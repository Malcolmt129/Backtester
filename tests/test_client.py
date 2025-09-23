from typing import assert_type
from src.client import IBClient 
from src.dbmanagement import DBManager
from ibapi.client import Contract
import pandas as pd
import pytest



class TestIBClient:

    
    def test_get_futures_contracts(self):

        db = DBManager()

        client = IBClient("127.0.0.1", 7497, 5, db)
        mnq = client._get_futures_contract('mnq')
        assert_type(mnq, Contract)
    

    def test_dataRequest(self):
        
        db = DBManager()

        client = IBClient("127.0.0.1", 7497, 5, db)
        data_mnq = client.dataRequest(90, 'mnq', durationStr= "1 D", barSizeSetting="5 mins")
        

        assert_type(data_mnq, pd.DataFrame)
        
