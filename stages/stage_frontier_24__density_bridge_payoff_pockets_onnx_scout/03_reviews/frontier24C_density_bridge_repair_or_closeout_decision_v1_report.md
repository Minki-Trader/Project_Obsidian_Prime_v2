# Frontier24C Density Bridge DD Repair Report(전선24C 빈도 연결 손실폭 수리 보고서)

Updated(갱신): 2026-06-14T08:15:34Z

Status(상태): `density_bridge_dd_repair_scout_clue_proxy_no_authority`

Judgment(판정): `scout_clue_preserved_clue_requires_closeout_no_authority`

Action(행동): F24B(전선24B)의 density bridge(빈도 연결) 후보에 train-only include/veto filter(학습 전용 포함/제외 필터)를 붙여 DD(drawdown, 손실폭) normalization repair(정규화 수리)를 실행했습니다.

Effect(효과): trade frequency(거래 빈도)를 유지한 상태에서 PF(profit factor, 수익 팩터)와 DD(drawdown, 손실폭)가 함께 좋아지는지 확인했습니다.

Source/filter/repair/metric rows(원천/필터/수리/지표 행): `18` / `96` / `220` / `660`

Density/scout/seed/handoff rows(빈도/탐색/씨앗/인계 행): `173` / `3` / `0` / `0`

Best repair(최상 수리): `f24c_0105`

Best validation PF/density/DD(최상 검증 수익 팩터/빈도/손실폭): `1.17717` / `6.7377/day` / `24.0994%`

Best OOS PF/density/DD(최상 표본외 수익 팩터/빈도/손실폭): `1.21164` / `7.29008/day` / `15.5702%`

Runtime probe status(런타임 탐침 상태): `out_of_scope_by_claim_no_handoff_candidate(인계 후보 없어 주장 범위 밖)`

## Top Repair Rows(상위 수리 행)

| repair(수리) | source bridge(원천 연결) | type(유형) | filter(필터) | val PF | val density | val DD | OOS PF | OOS density | OOS DD | DD relief | scout | seed |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `f24c_0105` | `f24b_0093` | veto | `atr_14_over_atr_50` | 1.17717 | 6.7377 | 24.0994 | 1.21164 | 7.29008 | 15.5702 | 5.77667 | True | False |
| `f24c_0106` | `f24b_0094` | veto | `atr_14_over_atr_50` | 1.17717 | 6.7377 | 24.0994 | 1.21164 | 7.29008 | 15.5702 | 5.77667 | True | False |
| `f24c_0163` | `f24b_0163` | veto | `atr_14_over_atr_50` | 1.1383 | 5.68852 | 23.1744 | 1.19709 | 6.06107 | 12.5059 | 6.13828 | True | False |
| `f24c_0208` | `f24b_0174` | veto | `hl_zscore_50` | 1.10416 | 6.98361 | 28.8156 | 1.27617 | 7.76336 | 18.4423 | 1.73968 | False | False |
| `f24c_0092` | `f24b_0146` | veto | `hl_zscore_50` | 1.19856 | 6.84699 | 28.1194 | 1.20963 | 7.29771 | 15.4302 | 1.7567 | False | False |
| `f24c_0093` | `f24b_0147` | veto | `hl_zscore_50` | 1.19856 | 6.84699 | 28.1194 | 1.20963 | 7.29771 | 15.4302 | 1.7567 | False | False |
| `f24c_0194` | `f24b_0174` | veto | `gap_percent` | 1.17727 | 7.84153 | 24.932 | 1.08493 | 8.56489 | 20.6437 | 5.62336 | False | False |
| `f24c_0155` | `f24b_0110` | veto | `gap_percent` | 1.18097 | 8.2459 | 26.0714 | 1.07064 | 8.74046 | 20.7042 | 5.538 | False | False |
| `f24c_0186` | `f24b_0174` | veto | `bollinger_width_20` | 1.05173 | 6.12022 | 14.3455 | 1.11235 | 7.19084 | 23.2924 | 7.26289 | False | False |
| `f24c_0096` | `f24b_0053` | veto | `usdx_zscore_20` | 1.24259 | 7.08197 | 31.6858 | 0.952915 | 7.45038 | 24.4701 | 4.41781 | False | False |
| `f24c_0097` | `f24b_0054` | veto | `usdx_zscore_20` | 1.24259 | 7.08197 | 31.6858 | 0.952915 | 7.45038 | 24.4701 | 4.41781 | False | False |
| `f24c_0206` | `f24b_0053` | include | `bb_position_20` | 1.26703 | 6.71585 | 28.8036 | 1.02541 | 7.48855 | 26.4951 | 7.30003 | False | False |

Next action(다음 행동): `frontier24D_stage_closeout_density_bridge_payoff_pockets_v1`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
