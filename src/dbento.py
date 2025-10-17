import databento as db
import pandas as pd
from keys import databento_key
import logging
from datetime import datetime

log = logging.getLogger(__name__)

class DataBento:

    
    
    def __init__(self):

        self.historicalClient = db.Historical(databento_key)


    def getFuturesExpSymbols(self, symbol: str, start, end):

        """
        Used to get futures contract symbols. In order to back adjust prices we have to know when
        the contracts expire and make an adjustment when the roll happens. This is builds the list
        so that we can do that seamlessly
        Args:

            dataset (str): Databento dataset to choose symbol from
            symbol (str): The symbol of the future to query
            start (?): Start of the lookback period, use yyyymmdd format
            end (?): End of the lookback period, use yyyymmdd format
        
        """

        try:
            wholeSymbol = symbol + ".FUT"

            data = self.historicalClient.timeseries.get_range(
                    dataset="GLBX.MDP3",
                    start= start,
                    end=end,
                    symbols=wholeSymbol,
                    stype_in="parent",
                    schema="definition",
                )
            df = data.to_df()

            df = df[df["instrument_class"] == db.InstrumentClass.FUTURE]
            df = df.set_index("expiration").sort_index()        
            
            return df["raw_symbol"].to_list()

        except Exception as e:
            log.error(f"@DBento.getFuturesExpSymbols(): {e}")
    


    
    def requestDailyFutureData(self, symbol: str, start: str, end: str):
        """
        Used to get daily futures data from DataBento within a specified time range.

        Args: 
            symbol (str): The symbol of the future to query
        """
        contSymbol = symbol + ".c.0"

        print(contSymbol)
        
        if self.is_date_valid(start) and self.is_date_valid(end):

            data: pd.DataFrame = self.historicalClient.timeseries.get_range(
                    dataset="GLBX.MDP3",
                    symbols=contSymbol,
                    stype_in="continuous",
                    schema="ohlcv-1d",
                    start=start,
                    end=end,

                    ).to_df()

            data = data.reset_index() #ts_event is the index of dataframe, this turns it back into col
            
            
            data["epoch_ts"] = data["ts_event"].astype("int64") // 10**9
            data['mid'] = (data['high'] + data['low'])/2 
            log.info(f"Request for{symbol} recieved...")

            return data

        else:
            print("Date probably doesn't exist, check start or end date")
            return pd.DataFrame()
    

    def backAdjustData(self, data: pd.DataFrame):

        """
        A helper function that will take in the data in a ohlcv format and back adjust all the
        to take out artificial spikes in prices. This should traverse the dataframe from the newest
        to oldest prices and take out the artificial jumps. 

        Args: 
            data(pd.DataFrame): Dataframe that gets passed in. 

        """
                
        # Sort descending so we start from latest and walk backward
        temp_df = data.sort_values("ts_event", ascending=False).copy()
        
        # This will accumulate the adjustment over time
        adjustment = 0.0
        adjusted_rows = []

        # Track the previous row
        prev_contract_id = None
        prev_close = None

        for i, row in temp_df.iterrows():
            current_contract_id = row["instrument_id"]
            current_close = row["close"]

            # If contract changes, calculate difference
            if prev_contract_id is not None and current_contract_id != prev_contract_id:
                diff = prev_close - current_close
                adjustment += diff
                print(f"Rolled contract at {row['ts_event']}: Adjusting by {diff}, total adjustment now {adjustment}")

            # Apply current total adjustment
            adjusted_row = row.copy()
            adjusted_row["close"] += adjustment
            adjusted_row["open"] += adjustment
            adjusted_row["high"] += adjustment
            adjusted_row["low"] += adjustment
            adjusted_row["mid"] += adjustment
            adjusted_rows.append(adjusted_row)

            # Update tracking
            prev_contract_id = current_contract_id
            prev_close = current_close

        adjusted_df = pd.DataFrame(adjusted_rows)
        
        # Re-sort into natural time order
        return adjusted_df.sort_values("ts_event")

    def requestAllDailyFuturesData(self, symbol: str):

        """ 
        TO DO:
        Function is not completely working yet...

        Used to get ALL daily futures data available for a certain contract.

        Args: 
            symbol (str): The symbol of the future to query
        """
    

        dataRange = self.historicalClient.metadata.get_dataset_range(dataset="GLBX.MDP3") 
        print("dataRange fine")

        startTime = pd.Timestamp(dataRange["start"])
        endTime = pd.Timestamp(dataRange["end"])
        
        contSymbol = symbol + ".c.0"

        
        data: pd.DataFrame = self.historicalClient.timeseries.get_range(
                dataset="GLBX.MDP3",
                symbols=contSymbol,
                stype_in="continuous",
                schema="ohlcv-1d",
                start=startTime,
                end=endTime,

                ).to_df()

        data = data.reset_index() #ts_event is the index of dataframe, this turns it back into col
        
        
        data["epoch_ts"] = data["ts_event"].astype("int64") // 10**9
        print(data)
        log.info(f"Request for{symbol} recieved...")

        return data


    def is_date_valid(self, date: str, fmt="%Y%m%d"):
        """
        This checks if the date is a valid date that exists. Like 09/31/2025 does not exist because
        september has only 30 days

        Args:
            date(str): The date string that needs to be checked
            fmt(str): The format of the date string 

        """
        try:
            datetime.strptime(date, fmt)
            return True

        except ValueError:
            return False


if __name__ == "__main__":
    dbe = DataBento()


    data = pd.read_csv("dailyDataWithRollovers.csv")
    adj_data = dbe.backAdjustData(data)
