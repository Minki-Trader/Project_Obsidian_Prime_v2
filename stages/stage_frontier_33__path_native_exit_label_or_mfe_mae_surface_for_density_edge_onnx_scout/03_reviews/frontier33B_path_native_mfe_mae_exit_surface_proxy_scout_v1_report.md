# Frontier33B Path-Native MFE/MAE Exit Surface Proxy Scout Report(전선33B 경로 기반 최대 유리/불리 이동 청산 표면 프록시 탐색 보고서)

Updated(갱신): 2026-06-14T14:00:57Z

Status(상태): `path_native_exit_surface_scout_only_no_runtime_candidate_no_authority`

Judgment(판정): `scout_clue_requires_repair_or_closeout_no_authority`

Action(행동): raw Bid OHLC path(원천 매수호가 시가/고가/저가/종가 경로)에서 MFE/MAE train-only quantile threshold(학습 전용 최대 유리/불리 이동 분위수 임계값)를 만들고, first-hit SL/TP path proxy(선터치 손절/익절 경로 프록시)를 실행했습니다.

Effect(효과): F32 return-space cap translation(수익률 공간 한도 번역)을 쓰지 않고, validation/OOS(검증/표본외)는 읽기 전용으로 path-native density edge(경로 기반 밀도 우위)를 확인합니다.

Condition/candidate/metric rows(조건/후보/지표 행): `640` / `247` / `741`

Path scout/seed/runtime candidate(경로 탐색/씨앗/런타임 후보): `4` / `0` / `0`

Strict DD candidate(엄격 손실폭 후보): `0`

Best candidate(최상 후보): `f33b_0176`

Best validation PF/density/DD(최상 검증 수익 팩터/밀도/손실폭): `1.121` / `7.956/day` / `14.816%`

Best OOS PF/density/DD(최상 표본외 수익 팩터/밀도/손실폭): `1.273` / `7.580/day` / `8.434%`

Best stop/take log thresholds(최상 손절/익절 로그 임계값): `0.003` / `0.004`

Runtime probe status(런타임 탐침 상태): `runtime_probe_out_of_scope_by_claim_path_native_scout_only_no_runtime_candidate`

## Top Readonly Forward Rows(상위 읽기 전용 전진 행)

| candidate(후보) | side(방향) | features(피처) | val PF | val density | val DD | OOS PF | OOS density | OOS DD | stop/take | scout | seed |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `f33b_0176` | short(숏) | `di_spread_14` | 1.121 | 7.956 | 14.816 | 1.273 | 7.580 | 8.434 | 0.003/0.004 | True | False |
| `f33b_0171` | short(숏) | `rsi_14` | 1.094 | 7.776 | 15.245 | 1.257 | 8.084 | 10.294 | 0.003/0.004 | True | False |
| `f33b_0172` | short(숏) | `rsi_14_minus_50` | 1.094 | 7.776 | 15.245 | 1.257 | 8.084 | 10.294 | 0.003/0.004 | True | False |
| `f33b_0192` | short(숏) | `vix_zscore_20` | 1.111 | 7.590 | 13.286 | 1.055 | 8.969 | 14.741 | 0.003/0.003 | True | False |
| `f33b_0246` | short(숏) | `roc_12` | 1.103 | 12.399 | 15.424 | 1.151 | 13.038 | 19.453 | 0.003/0.004 | False | False |
| `f33b_0237` | short(숏) | `vortex_indicator` | 1.066 | 12.891 | 14.410 | 1.152 | 13.374 | 20.062 | 0.003/0.003 | False | False |
| `f33b_0189` | short(숏) | `vix_zscore_20` | 1.118 | 12.885 | 17.450 | 1.060 | 14.840 | 22.064 | 0.003/0.003 | False | False |
| `f33b_0046` | short(숏) | `vortex_indicator` | 1.043 | 7.809 | 18.635 | 1.231 | 8.061 | 12.348 | 0.003/0.004 | False | False |
| `f33b_0216` | short(숏) | `us10yr_zscore_20` | 0.970 | 7.770 | 10.297 | 0.898 | 7.595 | 14.935 | 0.003/0.002 | False | False |
| `f33b_0181` | short(숏) | `roc_12` | 1.037 | 7.388 | 15.072 | 1.058 | 7.634 | 16.745 | 0.003/0.004 | False | False |
| `f33b_0190` | long(롱) | `return_1_over_atr_14` | 0.911 | 7.874 | 17.335 | 0.909 | 8.084 | 16.629 | 0.002/0.003 | False | False |
| `f33b_0177` | long(롱) | `ema20_ema50_spread_zscore_50` | 0.893 | 7.913 | 17.056 | 1.054 | 9.084 | 14.165 | 0.003/0.002 | False | False |

Next action(다음 행동): `frontier33C_path_native_exit_label_repair_or_closeout_decision_v1`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
