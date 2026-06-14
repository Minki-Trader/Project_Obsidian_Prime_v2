# Frontier20B Feature-State Rule Atlas Proxy Scout Report(전선20B 피처 상태 규칙 지도 프록시 탐색 보고서)

Updated(갱신): 2026-06-14T05:50:31Z

Status(상태): `rule_atlas_seed_surface_proxy_no_handoff_no_authority`

Judgment(판정): `seed_surface_candidate_high_dd_no_runtime_handoff_no_authority`

Action(행동): fixed 58 feature(고정 58 피처)에서 train-only quantile rule atlas(학습 전용 분위수 규칙 지도)를 만들고, train rank(학습 순위)로 고른 후보만 validation/OOS(검증/표본외)에 읽기 전용으로 재생했습니다.

Effect(효과): validation/OOS(검증/표본외) 성과로 규칙을 고르지 않으면서 seed surface(씨앗 표면)와 handoff candidate(인계 후보) 여부를 분리합니다.

Condition pool/candidate/metric rows(조건 풀/후보/지표 행): `45` / `533` / `1599`

Strict/seed/handoff counts(엄격/씨앗/인계 수): `0` / `19` / `0`

Best candidate(최상 후보): `f20b_pair_0359`

Best validation PF/density/DD(최상 검증 수익 팩터/빈도/손실폭): `1.32666` / `8.57923/day` / `31.7443%`

Best OOS PF/density/DD(최상 표본외 수익 팩터/빈도/손실폭): `1.22065` / `9.9084/day` / `20.7766%`

Runtime boundary(런타임 경계): `out_of_scope_by_claim_proxy_no_mt5(프록시 주장 범위라 MT5 없음)`

## Top Readonly Forward Rows(상위 읽기 전용 전진 행)

| candidate(후보) | side(방향) | rule(규칙) | val PF | val density | val DD | OOS PF | OOS density | OOS DD | seed |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `f20b_pair_0359` | long(롱) | `vix_zscore_20 <= q30 & close_ema50_ratio >= q70` | 1.32666 | 8.57923 | 31.7443 | 1.22065 | 9.9084 | 20.7766 | True |
| `f20b_pair_0446` | long(롱) | `ppo_hist_12_26_9 >= q70 & bb_position_20 >= q80` | 1.28978 | 7.36066 | 24.1437 | 1.21688 | 7.61069 | 15.5932 | True |
| `f20b_pair_0736` | long(롱) | `bb_position_20 >= q80 & vix_zscore_20 <= q20` | 1.38151 | 5.99454 | 19.814 | 1.21621 | 6.47328 | 17.6098 | True |
| `f20b_pair_0194` | long(롱) | `roc_12 >= q70 & vix_zscore_20 <= q30` | 1.21831 | 8.74317 | 31.7802 | 1.24943 | 9.76336 | 22.6897 | True |
| `f20b_pair_0337` | long(롱) | `vix_zscore_20 <= q30 & ppo_hist_12_26_9 >= q70` | 1.26295 | 8.01093 | 32.4684 | 1.26708 | 9.06107 | 18.401 | True |
| `f20b_pair_0455` | long(롱) | `ppo_hist_12_26_9 >= q70 & close_ema50_ratio >= q70` | 1.32552 | 7.54098 | 30.7073 | 1.21547 | 7.74046 | 14.9318 | True |
| `f20b_pair_0344` | long(롱) | `vix_zscore_20 <= q30 & ema9_ema20_diff >= q80` | 1.3785 | 7.48634 | 33.574 | 1.22867 | 9.16794 | 18.9702 | True |
| `f20b_pair_0345` | long(롱) | `vix_zscore_20 <= q30 & close_ema20_ratio >= q80` | 1.35448 | 7.02732 | 33.5013 | 1.28017 | 7.78626 | 18.0419 | True |
| `f20b_pair_0353` | long(롱) | `vix_zscore_20 <= q30 & close_ema50_ratio >= q80` | 1.42934 | 6.06557 | 29.8302 | 1.29085 | 7.47328 | 15.5502 | True |
| `f20b_pair_0739` | long(롱) | `bb_position_20 >= q80 & ppo_hist_12_26_9 >= q80` | 1.29862 | 5.59563 | 21.4615 | 1.2416 | 6 | 13.9881 | True |
| `f20b_pair_0052` | long(롱) | `vortex_indicator >= q70 & vix_zscore_20 <= q20` | 1.20625 | 6.21858 | 23.4841 | 1.20291 | 6.45802 | 15.6904 | True |
| `f20b_pair_0209` | long(롱) | `roc_12 >= q70 & vix_zscore_20 <= q20` | 1.2102 | 6.12022 | 24.867 | 1.24559 | 6.54962 | 17.8349 | True |

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
