from typing import Dict
import pandas as pd

from ..utils.types import MarketData, PatternSet
from ..indicators.core import sma


def is_uptrend_ma_alignment(close: pd.Series) -> bool:
    ma20 = sma(close, 20).iloc[-1]
    ma60 = sma(close, 60).iloc[-1]
    ma120 = sma(close, 120).iloc[-1]
    return bool(ma20 > ma60 > ma120)


def is_downtrend_ma_alignment(close: pd.Series) -> bool:
    ma20 = sma(close, 20).iloc[-1]
    ma60 = sma(close, 60).iloc[-1]
    ma120 = sma(close, 120).iloc[-1]
    return bool(ma20 < ma60 < ma120)


def detect_simple_n_pattern(close: pd.Series) -> bool:
    if len(close) < 30:
        return False
    a = close.iloc[-20]
    b = close.iloc[-10]
    c = close.iloc[-1]
    return bool(b > a and c > b)


def detect_w_pattern(close: pd.Series) -> bool:
    if len(close) < 60:
        return False
    roll_min = close.rolling(10).min()
    last = close.iloc[-1]
    recent_min = roll_min.iloc[-20:-5].min()
    prev_min = roll_min.iloc[-40:-25].min()
    return bool(last > close.mean() and abs(recent_min - prev_min) / close.mean() < 0.05)


def detect_cup_and_handle(close: pd.Series) -> bool:
    if len(close) < 120:
        return False
    ma = sma(close, 20)
    depth = (ma.max() - ma.min()) / ma.max()
    return bool(depth > 0.05 and depth < 0.35 and close.iloc[-1] > ma.iloc[-1])


def detect_inverse_head_shoulders(close: pd.Series) -> bool:
    if len(close) < 100:
        return False
    roll_min = close.rolling(5).min()
    left = roll_min.iloc[-70:-50].min()
    head = roll_min.iloc[-50:-30].min()
    right = roll_min.iloc[-30:-10].min()
    return bool(head < left and head < right and close.iloc[-1] > close.rolling(50).mean().iloc[-1])


class PatternDetector:
    def detect_all(self, market: MarketData) -> PatternSet:
        res: Dict[str, Dict[str, Dict]] = {}
        for symbol, df in market.candles.items():
            close = df["close"].dropna()
            res[symbol] = {
                "ma_alignment": {"up": is_uptrend_ma_alignment(close), "down": is_downtrend_ma_alignment(close)},
                "n_pattern": {"present": detect_simple_n_pattern(close)},
                "w_pattern": {"present": detect_w_pattern(close)},
                "cup_handle": {"present": detect_cup_and_handle(close)},
                "inv_head_shoulders": {"present": detect_inverse_head_shoulders(close)},
            }
        return PatternSet(patterns=res)