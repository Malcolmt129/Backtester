from dataclasses import dataclass
from pathlib import Path
from typing import cast
import tomllib
import pandas as pd
import numpy as np


_CONFIG_PATH = Path(__file__).parent.parent.parent / "config" / "dev.toml"

with open(_CONFIG_PATH, 'rb') as config:
    riskParams = tomllib.load(config)


@dataclass
class Position:
    instrument: str
    size: float
    price: float

@dataclass
class Account:
    cash: float
    positions: list[Position]




def calculate_total_capital(accounts: list[Account]) -> float:

    total = 0

    for account in accounts:
        total+= account.cash

    
    return total

def calculate_annualized_cash_vol_target(total_cash: float):
    
    return total_cash * (riskParams['risk']['cash_vol_pct']/100)





if __name__ == "__main__":
    pass
