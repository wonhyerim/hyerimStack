from dataclasses import dataclass
from typing import Dict, List
import pandas as pd


Symbol = str


@dataclass
class MarketData:
    candles: Dict[Symbol, pd.DataFrame]  # columns: [open, high, low, close, volume, value, foreign_net, inst_net]


@dataclass
class ScreenResult:
    passed: List[Symbol]
    metadata: Dict[Symbol, Dict[str, float]]


@dataclass
class PatternSet:
    patterns: Dict[Symbol, Dict[str, Dict]]  # pattern_name -> details


@dataclass
class Signals:
    entries: Dict[Symbol, pd.Series]
    exits: Dict[Symbol, pd.Series]


@dataclass
class BacktestResult:
    equity_curve: pd.Series
    trades: pd.DataFrame
    per_symbol: Dict[Symbol, Dict[str, float]]