import pytest
import pandas as pd
from src.dataEngine import DataEngine

@pytest.fixture 
def engine():
    
    return DataEngine

class TestDataEngine:
   

    def test_getData(self,engine):
       
        data = engine.getData()
        assert type(data) == pd.DataFrame
        assert "ts_event" in data.columns
        assert "rtype" in data.columns
        assert "publisher_id" in data.columns
        assert "instrument_id" in data.columns
        assert "open" in data.columns
        assert "high" in data.columns
        assert "low" in data.columns
        assert "close" in data.columns
        assert "volume" in data.columns
        assert "symbol" in data.columns
        assert "epoch_ts" in data.columns
        

     

        
