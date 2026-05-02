import sqlite3

from backtester.interfaces.databaseInterface import IDatabase
from backtester.instruments import Instrument
import logging
from backtester.messageBus import MessageBus
log = logging.getLogger(__name__)

#logging.basicConfig(level=logging.DEBUG)

class SQLiteManager(IDatabase):
    
    def __init__(self, bus: MessageBus, db_name: str = "tradingUniverse.db"):
        self.db_name = db_name
        self.bus = bus
        self.conn = sqlite3.connect(self.db_name) 
        self.cursor = self.conn.cursor()
        self.schema: dict[str,list[str]] = self._getSchema() 
        log.debug("Connected to DB")
        
        self.init_db()


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
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS instruments (
                ticker                TEXT PRIMARY KEY,
                contractType          TEXT NOT NULL,
                minSize               INTEGER NOT NULL,
                currentPrice          REAL NOT NULL,
                priceVolatility       REAL NOT NULL,
                executionCostPerBlock REAL NOT NULL
            );
        ''')
        self.conn.commit()
        log.warning("Created initial tables for database")
    

    """
    Instead of having all of these really specific queries in this class, why dont 
    I just verify that a query is valid. This means that I use the functionality
    already written with the sqlite3 class instead of me checking at each function
    """
    def execQuery(self, query: str, params:list) -> bool:
        try:

            """
            I need to see what happens when a query is executed. What gets returned?
            Where are the hiccups so that I can do this functionally. 

            """
            self.cursor.execute(query, params)
            return True

        except sqlite3.ProgrammingError as e:
            print(f"Error at verifyQuery: {e}")
            return False
   
    def load_instruments(self) -> dict[str, Instrument]:
        self.cursor.execute("SELECT * FROM instruments")
        return {row[0]: Instrument.from_row(row) for row in self.cursor.fetchall()}

    def _getSchema(self):
        tables = {}
        table_names = []
        # Execute the query to get table names
        self.cursor.execute("""
                            SELECT name FROM sqlite_master 
                            WHERE type='table'
                            AND name NOT LIKE 'sqlite_%';
                            """)
        table_names = self.cursor.fetchall()
        
        
        for (table,) in table_names:
            self.cursor.execute(f"PRAGMA table_info({table})")
            columns  = self.cursor.fetchall() 

            for column in columns:

            #this works because pragma returns (0, 'symbol', 'TEXT', 1, None, 0)
            # where the second parameter is the name of the column
                tables[table].append(column[1])
        
        return tables 

            
if __name__ == "__main__":
   pass 
    
