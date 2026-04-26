import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def getRawData(): 
    raw = pd.read_csv("../tests/dailyfuturedata.csv")
    raw.info() 

    
    return raw


def calculateSMAs(data: pd.DataFrame, fast: int, slow: int):

    data['SMA_fast'] = data['close'].rolling(fast).mean()
    data['SMA_slow'] = data['close'].rolling(slow).mean()

    return data

def plotData(data: pd.DataFrame):
    
    plt.style.use('seaborn-v0_8-darkgrid')
    plt.rcParams['savefig.dpi'] = 300
    plt.rcParams['font.family'] = "serif"
    
    ax = data[['close', 'SMA_fast', 'SMA_slow']].plot()
    plt.show()


def generateSignals(data: pd.DataFrame):

    data['position'] = np.where(data['SMA_fast'] > data['SMA_slow'], 1, -1)
    data.dropna(inplace=True)

    data['position'].plot(ylim=[-1.1, 1.1], title="Market Positioning", 
                          figsize=(10,6))

    data['returns'] = np.log(data['close'] / data['close'].shift(1))

    data['returns'].hist(bins=5, figsize=(10,6))
    plt.show()


def showResults(data: pd.DataFrame):

    data['strategy'] = data['position'].shift(1) * data['returns']

    print(data[['returns', 'strategy']].sum())
    print(data[['returns', 'strategy']].cumsum().apply(np.exp).plot(figsize=(10,6)))

if __name__ == "__main__": 

    raw = getRawData()
    raw_with_smas = calculateSMAs(raw, 4, 20)
    plotData(raw_with_smas)
    
    generateSignals(raw_with_smas)
    showResults(raw_with_smas)


