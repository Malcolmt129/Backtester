import sqlite3
from databaseInterface import IDatabase
import pandas as pd
import logging 



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
                volume              INTEGER NOT NULL
            );
        ''')
        self.conn.commit()
        log.debug("Created initial tables for database")

    def addDailyCandleData(self, contract: str, historicalData: pd.DataFrame):

        # Get the stock_id from the table... This means that I need to have all of the futures
        # contracts in the database beforehand
        try:

            for index, row in historicalData.iterrows():
                
                self.cursor.execute('''
                                INSERT INTO daily_futures_price_data (

                                symbol, timestamp, open, high, low, close, volume)
                                    VALUES (?, ?, ?, ?, ?, ?, ?)
                                ''',(contract, row['epoch_ts'], row["open"],
                                    row["high"], row["low"], row["close"], row["volume"]))
                self.conn.commit()
        
        except Exception as e:
            print("Error: ", e)
            log.info("Historical data was not successfully added to database")
                
        log.info("Historical data added to database")

    def getCandleData(self, start, end):
        pass
    
    
if __name__ == "__main__":
    db = DBManager() 
    db.init_db()
    
