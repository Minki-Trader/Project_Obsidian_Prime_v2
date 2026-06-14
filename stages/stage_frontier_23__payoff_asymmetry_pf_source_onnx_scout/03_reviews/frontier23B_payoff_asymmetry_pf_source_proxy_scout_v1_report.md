# Frontier23B Payoff Asymmetry PF Source Proxy Scout Report(전선23B 보상 비대칭 수익 팩터 원천 프록시 탐색 보고서)

Updated(갱신): 2026-06-14T07:25:45Z

Status(상태): `payoff_asymmetry_scout_clue_proxy_no_authority`

Judgment(판정): `scout_clue_requires_repair_or_closeout_no_authority`

Action(행동): train-only payoff asymmetry(학습 전용 보상 비대칭) 조건을 먼저 unconditional baseline(무조건 기준선)과 비교한 뒤, 통과 조건으로 단일/쌍 진입 상태 프록시를 탐색했습니다.

Effect(효과): validation/OOS(검증/표본외)는 선택에 쓰지 않고, forward diagnostic(전진 진단)으로만 보았습니다.

Pre-scout sanity gate(탐색 전 건전성 게이트): `True` with pass rows(통과 행) `78`.

Condition/candidate/metric rows(조건/후보/지표 행): `640` / `360` / `1080`

Scout/seed/handoff rows(탐색/씨앗/인계 행): `23` / `0` / `0`

Best candidate(최상 후보): `f23b_0333`

Best validation PF/density/DD(최상 검증 수익 팩터/빈도/손실폭): `1.27835` / `7.60109/day` / `19.1095%`

Best OOS PF/density/DD(최상 표본외 수익 팩터/빈도/손실폭): `1.07866` / `8.25191/day` / `15.4395%`

Runtime probe status(런타임 탐침 상태): `out_of_scope_by_claim_no_handoff_candidate_yet(인계 후보 전이라 주장 범위 밖)`

## Top Readonly Forward Rows(상위 읽기 전용 전진 행)

| candidate(후보) | side(방향) | features(피처) | val PF | val density | val DD | OOS PF | OOS density | OOS DD | scout | seed |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `f23b_0333` | long(롱) | `bb_position_20|vortex_indicator` | 1.27835 | 7.60109 | 19.1095 | 1.07866 | 8.25191 | 15.4395 | True | False |
| `f23b_0071` | long(롱) | `ppo_hist_12_26_9|vix_zscore_20` | 1.2574 | 8.56831 | 29.4714 | 1.15677 | 9.22901 | 20.3448 | True | False |
| `f23b_0226` | long(롱) | `rsi_14|vix_zscore_20` | 1.19101 | 10.2842 | 31.5915 | 1.07514 | 11.9542 | 23.5221 | True | False |
| `f23b_0227` | long(롱) | `rsi_14_minus_50|vix_zscore_20` | 1.19101 | 10.2842 | 31.5915 | 1.07514 | 11.9542 | 23.5221 | True | False |
| `f23b_0348` | long(롱) | `ema9_ema20_diff|bb_position_20` | 1.38409 | 5.81967 | 17.7272 | 1.07733 | 6.72519 | 14.259 | True | False |
| `f23b_0315` | long(롱) | `rsi_14|vix_zscore_20` | 1.32678 | 7.30601 | 29.0097 | 1.1263 | 8.16031 | 19.5223 | True | False |
| `f23b_0316` | long(롱) | `rsi_14_minus_50|vix_zscore_20` | 1.32678 | 7.30601 | 29.0097 | 1.1263 | 8.16031 | 19.5223 | True | False |
| `f23b_0098` | long(롱) | `vix_zscore_20|close_ema20_ratio` | 1.19679 | 9.97814 | 33.8124 | 1.05673 | 10.8855 | 27.1766 | True | False |
| `f23b_0101` | long(롱) | `roc_12|vix_zscore_20` | 1.17109 | 9.38798 | 32.8679 | 1.11612 | 10.2595 | 23.2183 | True | False |
| `f23b_0231` | long(롱) | `ppo_hist_12_26_9|vix_zscore_20` | 1.27248 | 5.99454 | 29.159 | 1.19289 | 6.68702 | 16.3815 | True | False |
| `f23b_0341` | long(롱) | `ema9_ema20_diff|ppo_hist_12_26_9` | 1.21876 | 7.36066 | 33.6055 | 1.11984 | 7.9313 | 16.8789 | True | False |
| `f23b_0167` | long(롱) | `vortex_indicator|vix_zscore_20` | 1.35647 | 5.56831 | 20.4647 | 1.05704 | 5.81679 | 14.115 | True | False |

Next action(다음 행동): `frontier23C_payoff_asymmetry_repair_or_closeout_decision_v1`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
