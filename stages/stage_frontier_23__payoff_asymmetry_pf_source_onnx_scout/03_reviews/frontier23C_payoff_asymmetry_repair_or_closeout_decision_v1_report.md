# Frontier23C Payoff Asymmetry Entry Filter Repair Report(전선23C 보상 비대칭 진입 필터 수리 보고서)

Updated(갱신): 2026-06-14T07:30:54Z

Status(상태): `payoff_asymmetry_entry_filter_repair_scout_clue_proxy_no_authority`

Judgment(판정): `preserved_clue_requires_closeout_no_authority`

Action(행동): F23B(전선23B) scout clue(탐색 단서)에 train-only include/veto filter(학습 전용 포함/제외 필터)를 붙여 entry-known repair(진입시점 수리)를 실행했습니다.

Effect(효과): seed(씨앗) 전 lifecycle repair(생명주기 수리) 없이 PF(수익 팩터), density(빈도), DD(손실폭)가 같이 좋아지는지 확인했습니다.

Source/repair/metric rows(원천/수리/지표 행): `16` / `240` / `720`

Scout/seed/handoff rows(탐색/씨앗/인계 행): `77` / `0` / `0`

Best repair(최상 수리): `f23c_0123`

Best validation PF/density/DD(최상 검증 수익 팩터/빈도/손실폭): `1.27966` / `7.57377/day` / `19.1095%`

Best OOS PF/density/DD(최상 표본외 수익 팩터/빈도/손실폭): `1.08388` / `8.17557/day` / `15.3161%`

Runtime probe status(런타임 탐침 상태): `out_of_scope_by_claim_no_handoff_candidate(인계 후보 없어 주장 범위 밖)`

## Top Repair Rows(상위 수리 행)

| repair(수리) | source(원천) | type(유형) | filter(필터) | val PF | val density | val DD | OOS PF | OOS density | OOS DD | scout | seed |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `f23c_0123` | `f23b_0333` | include | `close_ema20_ratio` | 1.27966 | 7.57377 | 19.1095 | 1.08388 | 8.17557 | 15.3161 | True | False |
| `f23c_0063` | `f23b_0333` | include | `rsi_14` | 1.27698 | 7.52459 | 19.1095 | 1.0659 | 8.16794 | 16.0428 | True | False |
| `f23c_0064` | `f23b_0333` | include | `rsi_14_minus_50` | 1.27698 | 7.52459 | 19.1095 | 1.0659 | 8.16794 | 16.0428 | True | False |
| `f23c_0080` | `f23b_0333` | veto | `trix_15` | 1.24094 | 7.32787 | 17.7272 | 1.07224 | 8.07634 | 16.2819 | True | False |
| `f23c_0233` | `f23b_0071` | veto | `usdx_zscore_20` | 1.32742 | 7.08743 | 29.5503 | 1.27317 | 6.8626 | 12.3762 | True | False |
| `f23c_0071` | `f23b_0333` | include | `vix_zscore_20` | 1.59163 | 3.89617 | 14.4954 | 1.23302 | 4.0687 | 12.3693 | True | False |
| `f23c_0209` | `f23b_0167` | include | `bb_position_20` | 1.59163 | 3.89617 | 14.4954 | 1.23302 | 4.0687 | 12.3693 | True | False |
| `f23c_0087` | `f23b_0333` | include | `vix_zscore_20` | 1.27563 | 6.28415 | 20.9579 | 1.18908 | 6.77863 | 15.5415 | True | False |
| `f23c_0060` | `f23b_0348` | include | `di_spread_14` | 1.38752 | 5.08197 | 16.8816 | 1.13372 | 5.94656 | 12.5774 | True | False |
| `f23c_0140` | `f23b_0348` | include | `di_spread_14` | 1.37856 | 5.71038 | 17.7272 | 1.08839 | 6.67939 | 14.259 | True | False |
| `f23c_0214` | `f23b_0333` | include | `vix_zscore_20` | 1.39404 | 5.2459 | 19.5709 | 1.21256 | 5.55725 | 14.5345 | True | False |
| `f23c_0144` | `f23b_0348` | veto | `trix_15` | 1.37643 | 5.79235 | 17.7272 | 1.07609 | 6.69466 | 14.259 | True | False |

Next action(다음 행동): `frontier23D_stage_closeout_payoff_asymmetry_pf_source_v1`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
