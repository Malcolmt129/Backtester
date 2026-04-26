from dataclasses import dataclass, field
from typing import cast
import pandas as pd
import numpy as np


"""
This is the dataclass that is going to be used to store the data that we
get from the database about certain instruments.

Before constructing an Instrument, use calculate_price_volatility(df) to
compute priceVolatility from a DataFrame of historical OHLCV data, then
store the result in the instruments table so it can be loaded via from_row().

params:
    ticker: str                 e.g. MES, MNQ...
    contractType: str           e.g. FUTURES, EQUITIES...
    minSize: int                The smallest unit you can buy(for blockValue cal)
    currentPrice: float         Used to derive blockValue
    priceVolatility: float      How much does the price of the instr. move
    executionCostPerBlock:float Half the typical spread
    blockValue: float           minSize x currentPrice (derived)
    icv: float                  blockValue x priceVolatility (derived)
    srUnitCost: float           2 x costPerBlock / (16 x icv) (derived)
"""


@dataclass
class Instrument:
    ticker: str
    contractType: str
    minSize: int
    currentPrice: float
    priceVolatility: float
    executionCostPerBlock: float
    blockValue: float = field(init=False)
    icv: float = field(init=False)
    srUnitCost: float = field(init=False)

    def __post_init__(self):
        self.blockValue = self.minSize * self.currentPrice
        self.icv = self.blockValue * self.priceVolatility
        self.srUnitCost = 2 * self.executionCostPerBlock / (16 * self.icv)

    @classmethod
    def from_row(cls, row: tuple) -> "Instrument":
        ticker, contractType, minSize, currentPrice, priceVolatility, executionCostPerBlock = row
        return cls(ticker, contractType, minSize, currentPrice, priceVolatility, executionCostPerBlock)


def calculate_price_volatility(df: pd.DataFrame):
    log_returns = cast(pd.Series,
                       np.log(df["close"] / df["close"].shift(1))
                       )
    return log_returns.rolling(window=25).std()


if __name__ == "__main__":
    print(
        calculate_price_volatility(
            pd.read_csv("../../tests/dailyfuturedata.csv")
        ))
