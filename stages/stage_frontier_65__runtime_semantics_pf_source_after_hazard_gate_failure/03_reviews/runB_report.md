# F65B Proxy-Runtime Gap Attribution(F65B 프록시-런타임 차이 귀속)

Updated(갱신): `2026-06-16T01:58:44Z`

Judgment(판정): `preserved_clue_sltp_unit_semantics_gap_no_authority(보존 단서, 손절/익절 단위 의미 차이, 권위 없음)`

## Action And Effect(행동과 효과)

Action(행동): F64E runtime telemetry(런타임 기록), expected signal summary(예상 신호 요약), proxy metrics(프록시 지표), MT5 deal history(MT5 거래 내역)를 같은 split(분할)별로 맞춰 차이를 층별로 분해했다.

Effect(효과): signal count gap(신호 수 차이)과 PF/DD economics gap(수익 팩터/손실폭 경제성 차이)을 분리했고, SL/TP unit semantics(손절/익절 단위 의미)가 1순위 원인 후보임을 기록했다.

## Layer Attribution(층별 귀속)

| split(분할) | raw adapter(원 어댑터) | veto(차단) | expected after veto(차단 후 예상) | entry transition block(진입 전환 차단) | actual non-flat(실제 비관망) | fills(체결) | PF gap(PF 차이) | DD gap(손실폭 차이) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| validation_is | 5269 | 1196 | 4073 | 2973 | 1100 | 1098 | -0.722671 | 23.9108 |
| oos | 4206 | 881 | 3325 | 2483 | 842 | 838 | -0.408076 | 4.76624 |

## Exit Shape(청산 형태)

| split(분할) | proxy stop%(프록시 손절률) | MT5 stop%(MT5 손절률) | proxy maxhold%(프록시 최대보유률) | MT5 maxhold%(MT5 최대보유률) | MT5 median duration sec(MT5 중앙 보유초) |
|---|---:|---:|---:|---:|---:|
| validation_is | 27.32% | 79.51% | 58.87% | 0.00% | 0 |
| oos | 28.10% | 67.54% | 56.73% | 0.00% | 0 |

## Main Read(주요 판독)

- feature_ready_diff(피처 준비 차이)는 `0/0`이므로 data coverage(데이터 커버리지)가 1순위 원인이 아니다.
- raw adapter signal(원 어댑터 신호)에서 runtime veto tape(런타임 차단 테이프) 차감, entry transition gate(진입 전환 게이트) 차감은 telemetry(런타임 기록)와 맞다.
- order fill gap(주문 체결 차이)는 작다. invalid stops(무효 손절)는 validation/OOS `2/4`건이다.
- MT5 exit shape(MT5 청산 형태)는 maxhold(최대 보유)가 `0`이고 대부분 SL/TP(손절/익절)로 몇 초 안에 끝났다.
- Proxy(프록시)는 40/60 price units(가격 단위) 최소 손절/익절처럼 계산했고, MT5는 180/280 points(포인트) 캡을 적용했다. `point=0.01`이면 실제 MT5 폭은 약 1.8/2.8 가격 단위다.

## Preserved Clue(보존 단서)

`sltp_unit_semantics_gap_between_proxy_price_units_and_mt5_points(프록시 가격 단위와 MT5 포인트 손절/익절 의미 차이)`

## Boundary(경계)

이 판정은 attribution scout(귀속 탐색) 전용이다. F65 targeted MT5 runtime probe(표적 MT5 런타임 탐침)는 아직 pending(대기)이다. completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음)이다.

Next run(다음 실행): `frontier65C_targeted_sltp_unit_runtime_probe_v1`.
