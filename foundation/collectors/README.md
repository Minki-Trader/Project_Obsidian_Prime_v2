# Collectors(수집 도구)

재사용 가능한 source loader(원천 로더), export reader(내보내기 판독기), raw normalization helper(원천 정규화 도우미)를 여기에 둔다.

단계 전용 일회성 메모(stage-specific one-off notes, 단계 전용 일회성 메모)는 이 폴더에 두지 않는다.

## Current Tools(현재 도구)

- `export_fpmarkets_v2_mt5_bars.py`: MetaTrader 5에서 브로커 원천 `M5` 봉(broker-native M5 bars, 브로커 원천 5분봉)을 `data/raw/mt5_bars/m5/`로 내보낸다.
- `raw_m5_inventory.py`: 기존 원천 `M5` CSV(csv, 표 파일)를 검사하고 단계 로컬 재고 보고서(stage-local inventory report, 단계 로컬 재고 보고서)를 쓴다.
- `time_semantics_probe.py`: 원천 timestamp(타임스탬프)가 UTC(협정세계시)처럼 동작하는지, 또는 브로커/서버 시계(broker/server clock, 브로커/서버 시계)처럼 동작하는지 검사한다.
