# Quant Pipeline

한국 주식 데이터를 대상으로 한 정량 트레이딩 파이프라인입니다. 데이터 수집 → 종목 스크리닝 → 패턴 탐지 → 매매 신호 생성 → 실행/포지션 관리 → 성과 분석을 메인 엔트리포인트에서 일괄 실행합니다.

## 디렉터리 구조
- `data`: 데이터 수집
  - `collector.py`: OHLCV, 거래대금(value), 외인/기관 순매매(현재는 모의 데이터 생성) + PyKrx 기반 분봉/수급 수집 유틸(`PyKrxCollector`)
- `indicators`: 기술적 지표
  - `core.py`: SMA, 볼린저밴드, 엔벨로프, 수익률, 이격도
- `screening`: 종목 스크리닝
  - `rankings.py`: 시총 근사(가격×거래량), 거래대금, 20일 모멘텀, 신고가 근접, 외인+기관 순매수 연속성 기반 점수화
- `patterns`: 패턴 탐지
  - `detector.py`: N/W 패턴, 컵핸들, 역 헤드앤숄더, 단기 정배열/장기 역배열
- `signals`: 매매 신호
  - `generator.py`: 스크리닝+패턴+지표(이평/볼린저/수급) 조합 진입·청산 신호
- `execution`: 실행/포지션 관리
  - `backtester.py`: 단순 롱온리 백테스터(일별 리밸런싱, 포지션 수 제한)
- `performance`: 성과 분석
  - `report.py`: 총수익, CAGR, 변동성, 샤프, MDD 및 최근 체결 내역 출력
- `utils`: 공용 타입 정의
  - `types.py`: `MarketData`, `ScreenResult`, `PatternSet`, `Signals`, `BacktestResult`
- 루트
  - `main.py`: 전체 파이프라인 오케스트레이션
  - `requirements.txt`

## 설치
가상환경 생성 및 의존성 설치:
```bash
sudo apt-get update -y && sudo apt-get install -y python3-venv
python3 -m venv /workspace/.venv
/workspace/.venv/bin/pip install -r /workspace/quant_pipeline/requirements.txt
```

## 실행
파이프라인 실행(모의 데이터 기준):
```bash
/workspace/.venv/bin/python -m quant_pipeline.main --symbols 005930 000660 035420 --start 2023-01-01 --end 2023-12-31 --capital 1000000
```

### PyKrx로 특정 날짜 분봉/수급 저장
입력한 날짜(YYYYMMDD)의 분봉 OHLCV, 거래대금, 거래량과 투자자(외국인/기관) 수급(일별)을 CSV로 저장합니다.
```bash
/workspace/.venv/bin/python -m quant_pipeline.main \
  --symbols 005930 000660 \
  --intraday-date 20250115 \
  --save-csv /workspace/krx_20250115.csv
```
- 저장 컬럼 예시: open, high, low, close, volume, value, foreign_value, inst_value, foreign_volume, inst_volume, foreign_net, inst_net, symbol
- 참고: 투자자 순매매는 PyKrx API 특성상 일 단위 합계를 분봉에 브로드캐스트하여 부착합니다.

## 커스터마이징 포인트
- 실데이터 연동: `data/collector.py`의 모의 데이터 생성 로직을 실제 데이터 소스(API/DB/CSV 등)로 교체
- 지표 확장: `indicators/core.py`에 신규 지표 추가 및 파라미터 튜닝
- 스크리닝/패턴/신호 로직 강화: `screening`, `patterns`, `signals` 하위 모듈 확장
- 백테스트 고도화: 수수료/슬리피지/리밸런싱 규칙/리스크 한도 등 `execution/backtester.py` 개선
- 리포트 확장: `performance/report.py`에서 그래프, 팩터별 성과, 종목별 상세 등 추가