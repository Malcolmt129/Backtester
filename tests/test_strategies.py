import pandas as pd
import numpy as np
from src.backtester.strategies.buyHold import calc_log_returns
import pytest


dataframe = pd.DataFrame({
        "open":   [100.0, 101.5, 103.0, 102.0, 104.5],
        "high":   [102.0, 103.5, 104.0, 104.0, 106.0],
        "low":    [ 99.0, 100.5, 101.5, 101.0, 103.5],
        "close":  [101.5, 103.0, 102.0, 104.5, 105.0],
        "volume": [500_000, 620_000, 480_000, 710_000, 550_000],
    }, index=pd.date_range("2024-01-01", periods=5, freq="D"))



def test_buyHold_calc_logReturns():
    df = dataframe.copy()
    expected = np.log(df["close"]/df["close"].shift(1))
    expected = pd.Series(expected)
    print(expected)
    result = calc_log_returns(df)
    assert expected.equals(result["log_returns"])


    
