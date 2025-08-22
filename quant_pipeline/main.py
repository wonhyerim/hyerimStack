import argparse
from typing import List

from .data.collector import DataCollector, PyKrxCollector
from .screening.rankings import RankingScreener
from .patterns.detector import PatternDetector
from .signals.generator import SignalGenerator
from .execution.backtester import Backtester
from .performance.report import PerformanceReporter


def run_pipeline(symbols: List[str], start: str, end: str, capital: float):
    collector = DataCollector()
    market = collector.fetch_market_data(symbols=symbols, start=start, end=end)

    screener = RankingScreener()
    screen_result = screener.screen(market)

    detector = PatternDetector()
    patterns = detector.detect_all(market)

    generator = SignalGenerator()
    signals = generator.generate(market, screen_result, patterns)

    backtester = Backtester(initial_capital=capital)
    bt_result = backtester.run(market, signals)

    reporter = PerformanceReporter()
    reporter.summarize(bt_result)


def fetch_intraday_and_save(symbols: List[str], date: str, out_csv: str):
    pyc = PyKrxCollector()
    pyc.fetch_and_save_for_date(symbols, date, out_csv_path=out_csv)


def parse_args():
    parser = argparse.ArgumentParser(description="Quant pipeline runner")
    parser.add_argument("--symbols", nargs="+", required=True, help="Symbols to run")
    parser.add_argument("--start", help="Start date YYYY-MM-DD")
    parser.add_argument("--end", help="End date YYYY-MM-DD")
    parser.add_argument("--capital", type=float, default=100000.0)
    parser.add_argument("--intraday-date", help="Fetch minute OHLCV for date YYYYMMDD and save")
    parser.add_argument("--save-csv", help="Path to save intraday CSV when --intraday-date is used")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.intraday_date and args.save_csv:
        fetch_intraday_and_save(symbols=args.symbols, date=args.intraday_date, out_csv=args.save_csv)
    else:
        if not args.start or not args.end:
            raise SystemExit("--start and --end are required for backtest mode. Or use --intraday-date with --save-csv.")
        run_pipeline(symbols=args.symbols, start=args.start, end=args.end, capital=args.capital)