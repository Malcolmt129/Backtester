import sqlite3

from pandas.core.reshape import encoding
from databaseInterface import IDatabase
import pandas as pd
import logging 
import pytz
from datetime import datetime, date, timedelta

log = logging.getLogger(__name__)

#logging.basicConfig(level=logging.DEBUG)

class DBManager(IDatabase):
    
    def __init__(self, db_name: str = "tradingUniverse.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name) 
        self.cursor = self.conn.cursor()
        
        log.debug("Connected to DB")


    def __exit__(self):
        self.close()

    
    def close(self):
        self.conn.commit()
        self.conn.close()
        log.debug("Database closed")
    
    def init_db(self):
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_futures_price_data (
                
                symbol              TEXT NOT NULL,
                timestamp           DECIMAL NOT NULL,
                open                DECIMAL NOT NULL, 
                high                DECIMAL NOT NULL,
                low                 DECIMAL NOT NULL,
                close               DECIMAL NOT NULL,
                mid,                DECIMAL NOT NULL, 
                volume              INTEGER NOT NULL
            );
        ''')
        self.conn.commit()
        log.warning("Created initial tables for database")

    def addDailyCandleData(self, contract: str, historicalData: pd.DataFrame):
        """
        Add Daily Candlestick data to database

        Args: 
            contract (str): The symbol of the futures being added to database. The contract terminology
            comes from when I was trying to get historical data from IBKR, may change later

            historicalData (pd.DataFrame): This data frame holds all the data from the daily futures
            data request. 

        """
        try:

            for _, row in historicalData.iterrows():
                
                query = f"""
                        INSERT INTO daily_futures_price_data (
                        symbol, timestamp, open, high, low, close, volume)
                        VALUES (?,?,?,?,?,?,?);"""

                self.cursor.execute(query,(contract, row['epoch_ts'], row["open"],
                                    row["high"], row["low"], row["close"], row["volume"]))
                self.conn.commit()
        
        except Exception as e:
            print("Error[addDailyCandleData] ", e)
            log.info("Historical data was not successfully added to database")
                
        log.info("Historical data added to database")

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
        
    
if __name__ == "__main__":
    db = DBManager() 
    db.init_db()
    
