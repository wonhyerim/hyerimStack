from typing import List, Dict, Optional
import pandas as pd
import numpy as np

from ..utils.types import MarketData
from ..utils.db import create_db_engine, ensure_intraday_table


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


class PyKrxCollector:
    def __init__(self):
        # Lazy import to avoid hard dependency if not used
        from pykrx import stock  # type: ignore
        self.stock = stock

    def fetch_minute_ohlcv(self, symbol: str, date_yyyymmdd: str) -> pd.DataFrame:
        # freq='m' returns minute bars for the specific date
        df = self.stock.get_market_ohlcv_by_date(date_yyyymmdd, date_yyyymmdd, symbol, freq="m")
        # Standardize columns to lower-case
        df = df.rename(columns={
            "시가": "open",
            "고가": "high",
            "저가": "low",
            "종가": "close",
            "거래량": "volume",
            "거래대금": "value",
        })
        return df

    def fetch_investor_flow_daily(self, symbol: str, date_yyyymmdd: str) -> pd.DataFrame:
        # 투자자별 거래량/거래대금 일자별 집계. detail=True로 분류 세분화 가능(버전 따라 다름)
        # 여기서는 일자 합계 기준 외국인/기관 순매매량 근사치를 생성
        val = self.stock.get_market_trading_value_by_date(date_yyyymmdd, date_yyyymmdd, symbol)
        vol = self.stock.get_market_trading_volume_by_date(date_yyyymmdd, date_yyyymmdd, symbol)
        # 컬럼명이 버전에 따라 다를 수 있어 안전하게 처리
        val_cols = val.columns.astype(str)
        vol_cols = vol.columns.astype(str)
        # 외국인, 기관 컬럼 추정
        foreign_col_val = next((c for c in val_cols if "외국인" in c), None)
        inst_col_val = next((c for c in val_cols if "기관" in c), None)
        foreign_col_vol = next((c for c in vol_cols if "외국인" in c), None)
        inst_col_vol = next((c for c in vol_cols if "기관" in c), None)
        res = pd.DataFrame(index=val.index)
        if foreign_col_val is not None:
            res["foreign_value"] = val[foreign_col_val]
        if inst_col_val is not None:
            res["inst_value"] = val[inst_col_val]
        if foreign_col_vol is not None:
            res["foreign_volume"] = vol[foreign_col_vol]
        if inst_col_vol is not None:
            res["inst_volume"] = vol[inst_col_vol]
        return res

    def fetch_and_save_for_date(self, symbols: List[str], date_yyyymmdd: str, out_csv_path: Optional[str] = None) -> Dict[str, pd.DataFrame]:
        results: Dict[str, pd.DataFrame] = {}
        for symbol in symbols:
            ohlcv_m = self.fetch_minute_ohlcv(symbol, date_yyyymmdd)
            flow_d = self.fetch_investor_flow_daily(symbol, date_yyyymmdd)
            # 분봉에 일별 수급을 동일 날짜로 join (시간별 세분 데이터가 없으므로 브로드캐스트)
            if not flow_d.empty:
                # flow_d는 보통 DatetimeIndex(일 단위) 한 줄일 수 있음
                for col in flow_d.columns:
                    if col.endswith("value"):
                        ohlcv_m[col] = float(flow_d[col].iloc[0])
                    else:
                        ohlcv_m[col] = float(flow_d[col].iloc[0])
                # 순매매량(근사) 컬럼 생성
                if "foreign_volume" in ohlcv_m.columns and "inst_volume" in ohlcv_m.columns:
                    ohlcv_m["foreign_net"] = ohlcv_m["foreign_volume"]
                    ohlcv_m["inst_net"] = ohlcv_m["inst_volume"]
            results[symbol] = ohlcv_m
        if out_csv_path:
            # 멀티심볼을 하나의 CSV로 저장: 심볼 컬럼 추가 후 concat
            frames = []
            for sym, df in results.items():
                dfx = df.copy()
                dfx["symbol"] = sym
                frames.append(dfx)
            if frames:
                all_df = pd.concat(frames)
                all_df.to_csv(out_csv_path, encoding="utf-8-sig")
        return results

    def save_intraday_to_db(self, db_url: str, symbols: List[str], date_yyyymmdd: str, table_name: str = "intraday_bars") -> None:
        engine = create_db_engine(db_url)
        ensure_intraday_table(engine, table_name=table_name)
        results = self.fetch_and_save_for_date(symbols, date_yyyymmdd, out_csv_path=None)
        rows = []
        for sym, df in results.items():
            if df.empty:
                continue
            # df index는 분 단위 시간. 문자열 또는 DatetimeIndex일 수 있음
            if not isinstance(df.index, pd.DatetimeIndex):
                # PyKrx는 보통 시각이 인덱스 문자열로 들어옴. 변환 시 날짜 정보가 필요함
                # 날짜+시간 결합: YYYYMMDD HH:MM 형태 지원 시 파싱
                try:
                    ts = pd.to_datetime(date_yyyymmdd + " " + df.index.astype(str), format="%Y%m%d %H%M")
                except Exception:
                    ts = pd.to_datetime(df.index)
            else:
                ts = df.index
            dfx = df.copy()
            dfx["symbol"] = sym
            dfx["ts"] = ts
            cols = [
                "symbol", "ts", "open", "high", "low", "close", "volume", "value",
                "foreign_value", "inst_value", "foreign_volume", "inst_volume", "foreign_net", "inst_net"
            ]
            for c in cols:
                if c not in dfx.columns:
                    dfx[c] = np.nan
            rows.append(dfx[cols])
        if not rows:
            return
        final_df = pd.concat(rows)
        # to_sql with if_exists append
        with engine.begin() as conn:
            final_df.to_sql(table_name, con=conn, if_exists="append", index=False)