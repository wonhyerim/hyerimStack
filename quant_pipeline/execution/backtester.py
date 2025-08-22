from typing import Dict
import pandas as pd
import numpy as np

from ..utils.types import MarketData, Signals, BacktestResult


class Backtester:
    def __init__(self, initial_capital: float = 100000.0, max_positions: int = 10):
        self.initial_capital = initial_capital
        self.max_positions = max_positions

    def run(self, market: MarketData, signals: Signals) -> BacktestResult:
        # Align index
        all_dates = None
        for df in market.candles.values():
            all_dates = df.index if all_dates is None else all_dates.union(df.index)
        all_dates = all_dates.sort_values()

        cash = self.initial_capital
        holdings: Dict[str, float] = {}
        equity_curve = []
        index_dates = []
        trades = []

        for date in all_dates:
            # price snapshot
            prices = {s: float(df.loc[date, "close"]) if date in df.index else np.nan for s, df in market.candles.items()}

            # process exits
            for symbol in list(holdings.keys()):
                exit_sig = signals.exits.get(symbol)
                if exit_sig is not None and date in exit_sig.index and exit_sig.loc[date] == 1:
                    qty = holdings.pop(symbol)
                    px = prices.get(symbol, np.nan)
                    if not np.isnan(px):
                        cash += qty * px
                        trades.append({"date": date, "symbol": symbol, "side": "SELL", "qty": qty, "price": px})

            # process entries, cap by max_positions
            open_slots = self.max_positions - len(holdings)
            if open_slots > 0:
                # symbols with entry today
                todays_entries = []
                for symbol, entry_ser in signals.entries.items():
                    if date in entry_ser.index and entry_ser.loc[date] == 1 and symbol not in holdings:
                        todays_entries.append(symbol)
                if len(todays_entries) > 0:
                    to_open = todays_entries[:open_slots]
                    alloc = cash / max(1, len(to_open))
                    for symbol in to_open:
                        px = prices.get(symbol, np.nan)
                        if np.isnan(px) or px <= 0:
                            continue
                        qty = alloc // px
                        if qty <= 0:
                            continue
                        cash -= qty * px
                        holdings[symbol] = qty
                        trades.append({"date": date, "symbol": symbol, "side": "BUY", "qty": qty, "price": px})

            # compute equity
            equity = cash + sum((prices.get(s, np.nan) * q if not np.isnan(prices.get(s, np.nan)) else 0) for s, q in holdings.items())
            equity_curve.append(equity)
            index_dates.append(date)

        equity_series = pd.Series(equity_curve, index=pd.Index(index_dates, name="date"))
        trades_df = pd.DataFrame(trades)
        per_symbol = {}
        if not trades_df.empty:
            for symbol, grp in trades_df.groupby("symbol"):
                buys = grp[grp["side"] == "BUY"]["qty"].sum()
                sells = grp[grp["side"] == "SELL"]["qty"].sum()
                per_symbol[symbol] = {"buys": float(buys), "sells": float(sells)}

        return BacktestResult(equity_curve=equity_series, trades=trades_df, per_symbol=per_symbol)