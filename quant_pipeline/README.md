# Quant Pipeline

Korean-stock oriented quant pipeline skeleton covering data collection, screening, pattern detection, signal generation, execution, and performance.

## Install

Create a venv and install requirements:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python -m quant_pipeline.main --symbols 005930 000660 --start 2022-01-01 --end 2023-12-31 --capital 1000000
```

Currently uses mock data; plug real data into `data/collector.py`.

## Structure

- data: collection interfaces
- indicators: technical indicators (SMA, Bollinger, envelopes)
- screening: ranking-based filters
- patterns: basic pattern detection (N/W, cup&handle, inverse H&S, MA alignment)
- signals: combines screen, patterns, indicators for entries/exits
- execution: simple backtester
- performance: reporting and metrics