# Frontier22B Session Return Shock PF Source Proxy Scout Report(전선22B 세션 수익률 충격 수익 팩터 원천 프록시 탐색 보고서)

Updated(갱신): 2026-06-14T06:46:04Z

Status(상태): `shock_pf_source_scout_clue_proxy_no_runtime_no_authority`

Judgment(판정): `scout_clue_requires_repair_or_closeout_no_authority`

Action(행동): shock condition(충격 조건) 1개와 context condition(문맥 조건) 1개를 결합한 후보를 train-only rank(학습 전용 순위)로 고르고, validation/OOS(검증/표본외)는 read-only diagnostic(읽기 전용 진단)으로만 봤습니다.

Effect(효과): F20 전체 규칙 지도 재탐색을 막고, PF edge(수익 팩터 우위)가 shock-anchored entry state(충격 고정 진입 상태)에서 나오는지 분리했습니다.

Condition/candidate/selected rows(조건/후보/선택 행): `37` / `464` / `156`

Scout/seed/handoff rows(탐색/씨앗/인계 행): `35` / `0` / `0`

F20 duplicate pressure rows(F20 중복 압력 행): `0`

Best candidate(최상 후보): `f22b_0379`

Best validation PF/density/DD(최상 검증 수익 팩터/빈도/손실폭): `1.45565` / `5.48087/day` / `17.9571%`

Best OOS PF/density/DD(최상 표본외 수익 팩터/빈도/손실폭): `1.1691` / `6.1145/day` / `15.5592%`

Runtime probe status(런타임 탐침 상태): `out_of_scope_by_claim_no_handoff_candidate_yet(인계 후보 전이라 주장 범위 밖)`

## Top Readonly Forward Rows(상위 읽기 전용 전진 행)

| candidate(후보) | lane(방향) | side(방향) | features(피처) | val PF | val density | val DD | OOS PF | OOS density | OOS DD | scout | seed |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `f22b_0379` | shock_continuation | long(롱) | `close_prev_close_ratio+ema20_ema50_diff` | 1.45565 | 5.48087 | 17.9571 | 1.1691 | 6.1145 | 15.5592 | True | False |
| `f22b_0321` | shock_continuation | long(롱) | `log_return_1+ema20_ema50_diff` | 1.45565 | 5.48087 | 17.9571 | 1.16655 | 6.10687 | 15.5592 | True | False |
| `f22b_0343` | shock_continuation | long(롱) | `log_return_1+mega8_pos_breadth_1` | 1.15121 | 10 | 29.6897 | 1.0606 | 9.37405 | 20.3051 | True | False |
| `f22b_0401` | shock_continuation | long(롱) | `close_prev_close_ratio+mega8_pos_breadth_1` | 1.15121 | 10 | 29.6897 | 1.0606 | 9.37405 | 20.3051 | True | False |
| `f22b_0263` | shock_continuation | long(롱) | `return_1_over_atr_14+ema20_ema50_diff` | 1.256 | 5.86885 | 20.3537 | 1.16426 | 6.64122 | 14.4093 | True | False |
| `f22b_0233` | shock_continuation | long(롱) | `return_1_over_atr_14+vix_zscore_20` | 1.11816 | 6.71038 | 21.1708 | 1.12254 | 6.9771 | 13.7344 | True | False |
| `f22b_0349` | shock_continuation | long(롱) | `close_prev_close_ratio+vix_zscore_20` | 1.19402 | 6.49727 | 26.0031 | 1.17343 | 6.72519 | 16.3352 | True | False |
| `f22b_0291` | shock_continuation | long(롱) | `log_return_1+vix_zscore_20` | 1.19427 | 6.4918 | 26.0031 | 1.17343 | 6.72519 | 16.3352 | True | False |
| `f22b_0147` | shock_continuation | long(롱) | `close_prev_close_ratio+ema20_ema50_diff` | 1.4812 | 3.51366 | 18.5485 | 1.33282 | 3.90076 | 13.0134 | True | False |
| `f22b_0205` | shock_continuation | long(롱) | `log_return_1+ema20_ema50_diff` | 1.4812 | 3.51366 | 18.5485 | 1.33282 | 3.90076 | 13.0134 | True | False |
| `f22b_0371` | shock_continuation | long(롱) | `close_prev_close_ratio+ema20_ema50_diff` | 1.4679 | 4.14208 | 19.9374 | 1.17849 | 5.0229 | 14.7939 | True | False |
| `f22b_0313` | shock_continuation | long(롱) | `log_return_1+ema20_ema50_diff` | 1.4679 | 4.14208 | 19.9374 | 1.17541 | 5.01527 | 14.8424 | True | False |

Next action(다음 행동): `frontier22C_shock_pf_source_repair_or_closeout_decision_v1`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
