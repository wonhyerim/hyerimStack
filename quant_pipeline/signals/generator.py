from typing import Dict
import pandas as pd

from ..utils.types import MarketData, ScreenResult, PatternSet, Signals
from ..indicators.core import sma, bollinger


class SignalGenerator:
    def generate(self, market: MarketData, screen: ScreenResult, patterns: PatternSet) -> Signals:
        entries: Dict[str, pd.Series] = {}
        exits: Dict[str, pd.Series] = {}
        for symbol, df in market.candles.items():
            if symbol not in screen.passed:
                entries[symbol] = pd.Series(0, index=df.index)
                exits[symbol] = pd.Series(0, index=df.index)
                continue

            close = df["close"]
            ma20 = sma(close, 20)
            mid, upper, lower = bollinger(close, 20, 2.0)
            flow = (df["foreign_net"] + df["inst_net"]).rolling(5).sum()
            pat = patterns.patterns.get(symbol, {})

            long_entry = (close > ma20) & (close.shift(1) <= ma20.shift(1))
            long_entry |= (close > upper) & (flow > 0)
            if pat.get("ma_alignment", {}).get("up"):
                long_entry |= close > mid
            if pat.get("n_pattern", {}).get("present"):
                long_entry |= close > close.shift(10)

            long_exit = (close < ma20) | (close < lower) | (flow < 0)

            entries[symbol] = long_entry.astype(int)
            exits[symbol] = long_exit.astype(int)

        return Signals(entries=entries, exits=exits)