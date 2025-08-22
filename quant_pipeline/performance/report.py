import pandas as pd

from ..utils.types import BacktestResult


class PerformanceReporter:
    def summarize(self, result: BacktestResult):
        eq = result.equity_curve
        if eq.empty:
            print("No results")
            return
        ret = eq.pct_change().fillna(0)
        total_return = eq.iloc[-1] / eq.iloc[0] - 1
        cagr = (1 + total_return) ** (252 / max(1, len(eq))) - 1
        vol = ret.std() * (252 ** 0.5)
        sharpe = ret.mean() / (ret.std() + 1e-9) * (252 ** 0.5)
        mdd = self.max_drawdown(eq)
        print(f"Total Return: {total_return:.2%}")
        print(f"CAGR: {cagr:.2%}")
        print(f"Volatility: {vol:.2%}")
        print(f"Sharpe: {sharpe:.2f}")
        print(f"Max Drawdown: {mdd:.2%}")
        if not result.trades.empty:
            print(result.trades.tail(10).to_string(index=False))

    @staticmethod
    def max_drawdown(equity: pd.Series) -> float:
        peak = equity.cummax()
        dd = equity / peak - 1
        return float(dd.min())