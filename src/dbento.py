import databento as dbe
import pandas as pd
from keys import databento_key
import pytz
from datetime import datetime, date, timedelta
import logging


log = logging.getLogger(__name__)

class DataBento:

    
    
    def __init__(self):

        self.historicalClient = dbe.Historical(databento_key)


    
    def requestDailyFutureData(self, symbol: str, start: str, end: str):

        data: pd.DataFrame = self.historicalClient.timeseries.get_range(
                dataset="GLBX.MDP3",
                symbols=symbol,
                stype_in="continuous",
                schema="ohlcv-1d",
                start=start,
                end=end

                ).to_df()

        data = data.reset_index() #ts_event is the index of dataframe, this turns it back into col

        data["epoch_ts"] = data["ts_event"].astype("int64") // 10**9
        
        log.info(f"Request for{symbol} recieved...")

        return data
    
    
    
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
    

if __name__ == "__main__":
    pass
