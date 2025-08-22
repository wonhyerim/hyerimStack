import argparse
from typing import List

from .data.collector import DataCollector
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


def parse_args():
    parser = argparse.ArgumentParser(description="Quant pipeline runner")
    parser.add_argument("--symbols", nargs="+", required=True, help="Symbols to run")
    parser.add_argument("--start", required=True, help="Start date YYYY-MM-DD")
    parser.add_argument("--end", required=True, help="End date YYYY-MM-DD")
    parser.add_argument("--capital", type=float, default=100000.0)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_pipeline(symbols=args.symbols, start=args.start, end=args.end, capital=args.capital)