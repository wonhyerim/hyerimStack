from typing import List, Dict
import pandas as pd
import numpy as np

from ..utils.types import MarketData


class DataCollector:
    def fetch_market_data(self, symbols: List[str], start: str, end: str) -> MarketData:
        # Mock data generator for demo; replace with real data source integration
        dates = pd.date_range(start=start, end=end, freq="B")
        candles: Dict[str, pd.DataFrame] = {}
        rng = np.random.default_rng(42)
        for symbol in symbols:
            price = 100 + np.cumsum(rng.normal(0, 1, size=len(dates)))
            high = price + rng.normal(0.2, 0.3, size=len(dates))
            low = price - rng.normal(0.2, 0.3, size=len(dates))
            open_ = price + rng.normal(0, 0.2, size=len(dates))
            volume = rng.integers(100000, 2000000, size=len(dates))
            value = volume * price
            foreign_net = rng.normal(0, 10000, size=len(dates))
            inst_net = rng.normal(0, 8000, size=len(dates))
            df = pd.DataFrame(
                {
                    "open": open_,
                    "high": high,
                    "low": low,
                    "close": price,
                    "volume": volume,
                    "value": value,
                    "foreign_net": foreign_net,
                    "inst_net": inst_net,
                },
                index=dates,
            )
            candles[symbol] = df
        return MarketData(candles=candles)