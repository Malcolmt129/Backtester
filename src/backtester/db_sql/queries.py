INSERT_INTO_DAILY_FUTURES = """
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

CREATE_1_MIN_FUTURES_TABLE = """
    CREATE TABLE IF NOT EXISTS futures_1min_price_data (
        symbol              TEXT NOT NULL,
        timestamp           DECIMAL NOT NULL,
        open                DECIMAL NOT NULL,
        high                DECIMAL NOT NULL,
        low                 DECIMAL NOT NULL,
        close               DECIMAL NOT NULL,
        volume              INTEGER NOT NULL
    );
"""

CREATE_5_MIN_FUTURES_TABLE = """
    CREATE TABLE IF NOT EXISTS futures_5min_price_data (
        symbol              TEXT NOT NULL,
        timestamp           DECIMAL NOT NULL,
        open                DECIMAL NOT NULL,
        high                DECIMAL NOT NULL,
        low                 DECIMAL NOT NULL,
        close               DECIMAL NOT NULL,
        volume              INTEGER NOT NULL
    );
"""

CREATE_BACKTEST_RUNS_TABLE = """
    CREATE TABLE IF NOT EXISTS backtest_runs (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        strategy        TEXT NOT NULL,
        symbol          TEXT NOT NULL,
        start_date      TEXT NOT NULL,
        end_date        TEXT NOT NULL,
        bars_processed  INTEGER NOT NULL,
        run_at          TEXT NOT NULL
    );
"""

INSERT_BACKTEST_RUN = """
    INSERT INTO backtest_runs (strategy, symbol, start_date, end_date, bars_processed, run_at)
    VALUES (?, ?, ?, ?, ?, ?);
"""

SELECT_ALL_BACKTEST_RUNS = """
    SELECT id, strategy, symbol, start_date, end_date, bars_processed, run_at
    FROM backtest_runs
    ORDER BY id DESC;
"""
