import pytest
from src.dbmanagement import DBManager
import sqlite3
import pandas as pd
class TestDBManager():

    def test_addDailyCandleData(self):
        db = DBManager(":memory:")
    
        db.cursor.execute('''
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
        db.conn.commit()

        sample_data = [
                ("ES", 1758412800, 100.25, 102.25, 99.5, 101.5, 99999),
                ("ES", 1758412810, 100.25, 102.25, 99.5, 101.5, 99999),
                ]


        mock_df = pd.DataFrame(sample_data, columns=["symbol", "epoch_ts", "open", "high", "low",
                                                     "close", "volume"])
        
        db.addDailyCandleData("ES", mock_df)
        
        
        check_query = """
                        SELECT * FROM daily_futures_price_data;
                      """
        
        return_df = pd.read_sql_query(check_query, db.conn)

        db.conn.close() #Need to close so that the in memory database is deleted

        assert(len(return_df) == len(sample_data))



    def test_getDailyCandleDataFromDB(self):

        db = DBManager(":memory:")


        db.cursor.execute('''
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

        sample_data = [
                ("ES", 1758412800, 100.25, 102.25, 99.5, 101.5, 99999),
                ("ES", 1758412810, 100.25, 102.25, 99.5, 101.5, 99999),
                ("ES", 1758412820, 100.25, 102.25, 99.5, 101.5, 99999),
                ("ES", 1758412830, 100.25, 102.25, 99.5, 101.5, 99999),
                ("ES", 1758412840, 100.25, 102.25, 99.5, 101.5, 99999),
                ("ES", 1758412850, 100.25, 102.25, 99.5, 101.5, 99999),
                ]   
        db.cursor.executemany("""
            INSERT INTO daily_futures_price_data (symbol, timestamp,open, high, low, close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, sample_data)
        
        db.conn.commit()
        
         
        df = db.getDailyCandleDataFromDB("ES", "20250920", "20250922")
        print(df)
        assert(len(df) == len(sample_data))
        db.conn.close() #Need to close so that the in memory database is deleted
        
