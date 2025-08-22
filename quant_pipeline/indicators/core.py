import pandas as pd


def sma(series: pd.Series, window: int) -> pd.Series:
    return series.rolling(window).mean()


def bollinger(series: pd.Series, window: int = 20, num_std: float = 2.0):
    mid = sma(series, window)
    std = series.rolling(window).std(ddof=0)
    upper = mid + num_std * std
    lower = mid - num_std * std
    return mid, upper, lower


def envelope(series: pd.Series, window: int = 20, pct: float = 0.02):
    mid = sma(series, window)
    upper = mid * (1 + pct)
    lower = mid * (1 - pct)
    return mid, upper, lower


def pct_change(series: pd.Series, periods: int = 1) -> pd.Series:
    return series.pct_change(periods)


def distance_from_ma(series: pd.Series, window: int) -> pd.Series:
    m = sma(series, window)
    return (series - m) / m