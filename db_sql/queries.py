
INSERT_INTO_DAILY_FUTURES =  """

    INSERT INTO daily_futures_price_data (
    symbol, timestamp, open, high, low, close, volume)
    VALUES (?,?,?,?,?,?,?);

"""

CREATE_DAILY_FUTURES_TABLE = """

    CREATE TABLE IF NOT EXISTS daily_futures_price_data (
        
        symbol              TEXT NOT NULL,
        timestamp           DECIMAL NOT NULL,
        open                DECIMAL NOT NULL, 
        high                DECIMAL NOT NULL,
        low                 DECIMAL NOT NULL,
        close               DECIMAL NOT NULL,
        volume              INTEGER NOT NULL
    );
"""
