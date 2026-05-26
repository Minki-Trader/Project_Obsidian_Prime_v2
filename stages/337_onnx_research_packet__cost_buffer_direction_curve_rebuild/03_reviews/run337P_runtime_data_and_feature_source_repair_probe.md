# Stage337P Runtime Data And Feature Source Repair Probe(337P 런타임 데이터 및 피처 원천 수리 탐침)

- run_id(실행 ID): `run337P_materialize_runtime_data_and_feature_source_repair_probe_v1`
- status(상태): `completed_stage337P_asof_feature_source_repair_probe_runtime_completed_tester_gap_remains_no_forward_decision`
- judgment(판정): `asof_macro_core56_source_repair_runtime_probe_completed_current_day_tester_gap_requires_review`
- decision(결정): `stage337P_open_run337Q_repair_probe_review_no_selection`
- latest US100 close(최신 US100 종가): `2026-05-27T02:00:00Z`
- MT5 completed(MT5 완료): `5/5`
- tester current-day gap attempts(테스터 현재일 공백 시도): `5`
- raw proxy parity(전체 프록시 동등성): `10/25`
- timestamp-aligned proxy parity(시점 맞춤 프록시 동등성): `25/25`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Feature Sources(피처 원천)

| feature_set(피처 세트) | policy(정책) | rows(행) | last(마지막) | max_age(최대 나이) |
|---|---:|---:|---:|---:|
| `core56_no_top3_weight_features` | `asof_source_repair_probe` | `3264` | `2026-05-27T02:00:00+00:00` | `5370.0` |
| `macro48_no_equity_breadth_or_top3` | `asof_source_repair_probe` | `8010` | `2026-05-27T02:00:00+00:00` | `3065.0` |
| `us100_technical42_no_external` | `exact_us100_current_day_tester_gap_probe` | `8094` | `2026-05-27T02:00:00+00:00` | `0.0` |

## Runtime Metrics(런타임 지표)

| attempt(시도) | status(상태) | net(순익) | PF(손익비) | trades(거래수) | DD(드로다운) |
|---|---:|---:|---:|---:|---:|
| `c56_bal_rf` | `completed/completed/completed` | `-49.0` | `0.87` | `80` | `126.68` |
| `c56_plain_rf` | `completed/completed/completed` | `146.56` | `1.67` | `84` | `63.32` |
| `m48_bal_rf` | `completed/completed/completed` | `-17.63` | `0.98` | `351` | `113.73` |
| `m48_plain_rf` | `completed/completed/completed` | `267.39` | `1.4` | `344` | `91.32` |
| `u42_plain_rf` | `completed/completed/completed` | `99.9` | `1.13` | `344` | `112.86` |

## Boundary(경계)

as-of source repair(시점 기준 원천 수리)는 feature handoff(피처 인계) 수리 탐침일 뿐이다. timestamp-aligned proxy parity(시점 맞춤 프록시 동등성)는 tester observed window(테스터 관측 구간)에 맞춘 실행 의미 확인이다. model training(모델 학습), threshold retuning(임계값 재조정), lot optimization(랏 최적화), Forward Passed/Failed(전진 통과/실패)는 수행하지 않는다.
