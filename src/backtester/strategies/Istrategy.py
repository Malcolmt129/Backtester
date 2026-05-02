from dataclasses import dataclass
from typing import Callable
import pandas as pd


@dataclass
class Strategy:
    name: str
    run: Callable[[pd.DataFrame], pd.DataFrame]


