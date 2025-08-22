from typing import Dict, List
import pandas as pd

from ..utils.types import MarketData, ScreenResult


class RankingScreener:
    def screen(self, market: MarketData) -> ScreenResult:
        metrics: Dict[str, Dict[str, float]] = {}
        for symbol, df in market.candles.items():
            mcap = (df["close"] * df["volume"]).rolling(20).mean().iloc[-1]
            turnover = df["value"].rolling(20).mean().iloc[-1]
            momentum = df["close"].pct_change(20).iloc[-1]
            breakout = float(df["close"].iloc[-1] >= df["close"].rolling(252).max().iloc[-1] * 0.99)
            net_buy_streak = int((df["foreign_net"] + df["inst_net"]).tail(10).gt(0).sum())
            metrics[symbol] = {
                "mcap": float(mcap),
                "turnover": float(turnover),
                "momentum": float(momentum),
                "breakout": float(breakout),
                "net_buy_streak_10": float(net_buy_streak),
            }

        # Simple scoring combining ranks
        metrics_df = pd.DataFrame.from_dict(metrics, orient="index")
        ranks = metrics_df.rank(ascending=False)
        score = ranks.sum(axis=1)
        top = score.nsmallest(max(1, int(len(score) * 0.4))).index.tolist()
        return ScreenResult(passed=top, metadata=metrics)