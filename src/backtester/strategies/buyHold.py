from .Istrategy import Strategy
import pandas as pd
import numpy as np
from typing import cast


"""
    This function will take in a pandas DataFrame, and create another row for 
    the log returns.
    
    Parameters
    ------------------------
    df: pd.Dataframe
    Will take the shape of OHLCV
    

    Returns
    ------------------------
    pd.DataFrame with column for log_returns

    
"""
def calc_log_returns(df: pd.DataFrame) -> pd.DataFrame:
    returnDf = df.copy()
    returnDf['log_returns']  = np.log(returnDf["close"] / returnDf["close"].shift(1))
    return returnDf 



"""
    This function will take in a pandas DataFrame, and output a forecast between
    the ranges of -20 and 20. The forecast should not a magnitude greater than 
    20
    
    Parameters
    ------------------------
    data: pd.Dataframe
    Will take the shape of OHLCV
    

    Returns
    ------------------------
    forecast: int
"""

def calc_forecast(data: pd.DataFrame) -> int:
    forecast = 0


    return forecast



#Not finished implementing
def run_monteCarlo_sim(data: pd.DataFrame, 
                       startingPrice: float, 
                       seed: int = 42, 
                       days: int = 256, 
                       simulations: int = 1000, 
                       ):
    df = data.copy()

    # Parameter estimation
    mu = df["log_returns"].dropna().mean() #daily mean
    sigma = df["log_returns"].std() #daily volatility
    
    rng = np.random.default_rng(seed)

    dailyReturns = rng.normal(mu, sigma, size=(days, simulations))
    pricePaths = startingPrice * np.exp(np.cumsum(dailyReturns, axis=0))

    return pricePaths

    

    
    




