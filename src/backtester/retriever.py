import pandas as pd


# I think I should use a list to send all of the queries to the database
# instance.
def addDailyCandleData(self, contract: str, historicalData: pd.DataFrame)-> list[tuple]:
    """
    Add Daily Candlestick data to database

    Args: 
        contract (str): The symbol of the futures being added to database. The contract terminology
        comes from when I was trying to get historical data from IBKR, may change later

        historicalData (pd.DataFrame): This data frame holds all the data from the daily futures
        data request. 

    """

    queries = []
    try:

        for _, row in historicalData.iterrows():
            
            query = f"""
                    INSERT INTO daily_futures_price_data (
                    symbol, timestamp, open, high, low, close, volume)
                    VALUES (?,?,?,?,?,?,?);"""

            self.cursor.execute(query,(contract, row['epoch_ts'], row["open"],
                                row["high"], row["low"], row["close"], row["volume"])           k)
            self.conn.commit()
    
    except Exception as e:
        print("Error[addDailyCandleData] ", e)
            

def getDailyCandleDataFromDB(self, symbol: str,  start: str, end: str) -> pd.DataFrame:
        """
        Retrieve daily candle data FROM the database to use for analysis     
        
        Args:
            symbol(str): Symbol of the data we are trying to analyze
            start(str): Start of lookback period, use yyyymmdd format
            end(str): End of lookback period, use yyyymmdd format

        """
        start_epoch = datetime.strptime(start, "%Y%m%d")
        start_epoch = start_epoch.timestamp()
        end_epoch = datetime.strptime(end, "%Y%m%d")
        end_epoch = end_epoch.timestamp()

        print(f"start_epoch: {start_epoch} and end_epoch: {end_epoch}")
        query = f"""
                SELECT * 
                FROM daily_futures_price_data
                WHERE 
                symbol = ? 
                AND timestamp BETWEEN ? AND ?
                """
        df = pd.read_sql_query(query, self.conn, params=(symbol, start_epoch, end_epoch))

        print(df)
        return df
