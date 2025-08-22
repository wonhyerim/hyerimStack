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


def fetch_intraday_and_save(symbols: List[str], date: str, out_csv: str | None, db_url: str | None, table: str | None):
    pyc = PyKrxCollector()
    if db_url:
        pyc.save_intraday_to_db(db_url=db_url, symbols=symbols, date_yyyymmdd=date, table_name=table or "intraday_bars")
    if out_csv:
        pyc.fetch_and_save_for_date(symbols, date, out_csv_path=out_csv)


def parse_args():
    parser = argparse.ArgumentParser(description="Quant pipeline runner")
    parser.add_argument("--symbols", nargs="+", required=True, help="Symbols to run")
    parser.add_argument("--start", help="Start date YYYY-MM-DD")
    parser.add_argument("--end", help="End date YYYY-MM-DD")
    parser.add_argument("--capital", type=float, default=100000.0)
    parser.add_argument("--intraday-date", help="Fetch minute OHLCV for date YYYYMMDD and save")
    parser.add_argument("--save-csv", help="Path to save intraday CSV when --intraday-date is used")
    parser.add_argument("--db-url", help="MariaDB URL, e.g., mysql+pymysql://user:pass@host:3306/dbname")
    parser.add_argument("--table", help="DB table name for intraday (default: intraday_bars)")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.intraday_date:
        fetch_intraday_and_save(symbols=args.symbols, date=args.intraday_date, out_csv=args.save_csv, db_url=args.db_url, table=args.table)
    else:
        if not args.start or not args.end:
            raise SystemExit("--start and --end are required for backtest mode. Or use --intraday-date.")
        run_pipeline(symbols=args.symbols, start=args.start, end=args.end, capital=args.capital)