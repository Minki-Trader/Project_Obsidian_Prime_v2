# Raw M5 Inventory(원천 M5 재고)

## 요약(Summary, 요약)

- 상태(status, 상태): `complete`
- 원천 위치(raw root, 원천 위치): `data/raw/mt5_bars/m5`
- 예상 심볼 수(expected symbols, 예상 심볼 수): `12`
- 사용 가능 심볼 수(usable symbols, 사용 가능 심볼 수): `12`
- 공통 첫 봉(common first open, 공통 첫 봉): `2022-08-01T16:35:00Z`
- 공통 마지막 봉(common last open, 공통 마지막 봉): `2026-04-13T22:55:00Z`
- US100 첫 봉(US100 first open, US100 첫 봉): `2022-08-01T01:00:00Z`
- US100 마지막 봉(US100 last open, US100 마지막 봉): `2026-04-13T23:55:00Z`

## 경계(Boundary, 경계)

이 결과는 원천 재고(raw inventory, 원천 재고)만 말한다. 피처 준비(feature readiness, 피처 준비), 모델 준비(model readiness, 모델 준비), 런타임 권위(runtime authority, 런타임 권위), 운영 승격(operating promotion, 운영 승격)은 주장하지 않는다.

## 심볼별 표(Symbol Table, 심볼별 표)

| symbol(심볼) | broker(브로커) | status(상태) | rows(행 수) | first open(첫 봉) | last open(마지막 봉) | manifest(목록 파일) | timing notes(시간 메모) |
|---|---|---:|---:|---|---|---|---|
| `US100` | `US100` | `usable_raw_inventory` | 261345 | `2022-08-01T01:00:00Z` | `2026-04-13T23:55:00Z` | `ok` | gaps=967 |
| `VIX` | `VIX` | `usable_raw_inventory` | 158415 | `2022-08-01T01:00:00Z` | `2026-04-13T23:55:00Z` | `ok` | gaps=29475 |
| `US10YR` | `US10YR` | `usable_raw_inventory` | 223363 | `2022-08-01T01:00:00Z` | `2026-04-13T23:55:00Z` | `ok` | gaps=23003 |
| `USDX` | `USDX` | `usable_raw_inventory` | 238993 | `2022-08-01T03:00:00Z` | `2026-04-13T23:55:00Z` | `ok` | gaps=1057 |
| `NVDA` | `NVDA.xnas` | `usable_raw_inventory` | 71046 | `2022-08-01T16:35:00Z` | `2026-04-13T22:55:00Z` | `ok` | gaps=934 |
| `AAPL` | `AAPL.xnas` | `usable_raw_inventory` | 71935 | `2022-08-01T16:30:00Z` | `2026-04-13T22:55:00Z` | `ok` | gaps=938 |
| `MSFT` | `MSFT.xnas` | `usable_raw_inventory` | 71910 | `2022-08-01T16:30:00Z` | `2026-04-13T22:55:00Z` | `ok` | gaps=936 |
| `AMZN` | `AMZN.xnas` | `usable_raw_inventory` | 71933 | `2022-08-01T16:30:00Z` | `2026-04-13T22:55:00Z` | `ok` | gaps=939 |
| `AMD` | `AMD.xnas` | `usable_raw_inventory` | 71932 | `2022-08-01T16:30:00Z` | `2026-04-13T22:55:00Z` | `ok` | gaps=938 |
| `GOOGL.xnas` | `GOOGL.xnas` | `usable_raw_inventory` | 71917 | `2022-08-01T16:30:00Z` | `2026-04-13T22:55:00Z` | `ok` | gaps=936 |
| `META` | `META.xnas` | `usable_raw_inventory` | 71916 | `2022-08-01T16:30:00Z` | `2026-04-13T22:55:00Z` | `ok` | gaps=937 |
| `TSLA` | `TSLA.xnas` | `usable_raw_inventory` | 71916 | `2022-08-01T16:30:00Z` | `2026-04-13T22:55:00Z` | `ok` | gaps=937 |

## 해석(Read, 해석)

- `gaps`는 휴장, 세션 차이, 종목 거래시간 차이 때문에 생길 수 있는 앞으로 건너뛴 간격(forward gap, 전진 간격)이다.
- `ok`는 파일 구조와 manifest(목록 파일)가 관측값과 맞는다는 뜻이다.
- 시간대(timezone, 시간대)는 아직 원천 export(내보내기)의 `UNRESOLVED_REQUIRES_MANUAL_BINDING` 값을 유지한다.
