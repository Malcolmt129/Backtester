import sqlite3
import pandas as pd
from src.databaseInterface import IDatabase

class DBManager(IDatabase):
    
    def __init__(self, db_name: str = "tradingUniverse.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name) 
        self.cursor = self.conn.cursor()
    


    def __exit__(self):
        self.close()

    
    def close(self):
        self.conn.commit()
        self.conn.close()

    
    def init_db(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS futures_contracts (
                id_num      INTEGER PRIMARY KEY AUTOINCREMENT,
                ticker      VARCHAR(8) UNIQUE
            ); 
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS future_price_data (
                id INTEGER PRIMARY KEY,
                stock_id    INTEGER, 
                timestamp   TEXT NOT NULL,
                open        REAL NOT NULL, 
                high        REAL NOT NULL,
                low         REAL NOT NULL,
                close       REAL NOT NULL,
                volume      REAL NOT NULL,
                granularity TEXT NOT NULL
            );
        ''')

        self.conn.commit()
        self._addSymbolsToDB()

    def _addSymbolsToDB(self):
            
        futures_symbols = [ "ES", "NQ", "GC", "ZB", "ZC", "ZS", "ZW" ] 
        
        try: 
            for symbol in futures_symbols: 
                self.cursor.execute('''
                    INSERT OR IGNORE INTO futures_contracts (ticker) VALUES (?)
                ''', (symbol,)) # Need to have a trailing comma, remember
                print(f"Added {symbol} contract to database")

        except Exception as e:
                print("Error: ", e)

        self.conn.commit()

    def addCandleData(self, dataFrame: pd.DataFrame):

        
        # Get the stock_id from the table... This means that I need to have all of the futures
        # contracts in the database beforehand

        self.cursor.execute('''
                        INSERT INTO future_price (

                        stock_id, timestamp, open, high, low, close, volume, granularity )
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        ''', ())
    
    def getCandleData(self, start, end):
        pass

if __name__ == "__main__":
    db = DBManager() 
    db.init_db()
