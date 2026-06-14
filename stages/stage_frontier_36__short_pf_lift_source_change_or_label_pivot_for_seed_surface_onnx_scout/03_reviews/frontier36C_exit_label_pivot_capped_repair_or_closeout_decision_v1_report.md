# Frontier36C Exit Label Pivot Repair Report(전선36C 청산 라벨 전환 수리 보고)

Updated(갱신): 2026-06-14T16:33:04Z

Status(상태): `exit_label_pivot_capped_repair_closeout_queued_no_authority`

Judgment(판정): `label_pivot_repair_expanded_scout_but_no_seed_runtime_requires_closeout`

Action(행동): scout rows(탐색 행)에 새 피처 필터를 얹지 않고 stop/take label grid(손절/익절 라벨 격자)만 전환했습니다.

Effect(효과): DD/PF/density(손실폭/수익 팩터/밀도)가 청산 라벨 변화만으로 seed surface(씨앗 표면)에 가까워지는지 분리해 봅니다.

Candidate/scout/near-seed/seed/runtime rows(후보/탐색/근접 씨앗/씨앗/런타임 행): `320` / `132` / `1` / `0` / `0`

Best read-only candidate(최상 읽기 전용 후보): `f36c_0124`

Best validation PF-density-DD(최상 검증 수익 팩터-밀도-손실폭): `1.123` / `5.115/day` / `9.191%`

Best OOS PF-density-DD(최상 표본밖 수익 팩터-밀도-손실폭): `1.138` / `5.718/day` / `7.706%`

Runtime probe status(런타임 탐침 상태): `runtime_probe_out_of_scope_by_claim_capped_repair_no_runtime_candidate`

| candidate(후보) | source(원천) | features(피처) | val PF | val density | val DD | OOS PF | OOS density | OOS DD | scout | near seed | seed |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `f36c_0124` | `f36b_0004` | `vortex_indicator|vix_zscore_20` | 1.123 | 5.115 | 9.191 | 1.138 | 5.718 | 7.706 | True | True | False |
| `f36c_0175` | `f36b_0016` | `vix_zscore_20|di_spread_14` | 1.083 | 7.585 | 8.032 | 1.086 | 8.443 | 8.831 | True | False | False |
| `f36c_0144` | `f36b_0016` | `vix_zscore_20|di_spread_14` | 1.073 | 7.585 | 8.778 | 1.072 | 8.443 | 8.214 | True | False | False |
| `f36c_0118` | `f36b_0016` | `vix_zscore_20|di_spread_14` | 1.113 | 7.585 | 7.445 | 1.054 | 8.443 | 9.150 | True | False | False |
| `f36c_0110` | `f36b_0016` | `vix_zscore_20|di_spread_14` | 1.098 | 7.585 | 8.607 | 1.079 | 8.443 | 9.780 | True | False | False |
| `f36c_0143` | `f36b_0194` | `di_spread_14|roc_12` | 1.068 | 8.781 | 12.551 | 1.156 | 9.336 | 8.147 | True | False | False |
| `f36c_0090` | `f36b_0006` | `vix_zscore_20|vortex_indicator` | 1.087 | 7.366 | 6.792 | 1.081 | 8.252 | 9.421 | True | False | False |
| `f36c_0235` | `f36b_0016` | `vix_zscore_20|di_spread_14` | 1.063 | 7.585 | 9.083 | 1.077 | 8.443 | 8.445 | True | False | False |
| `f36c_0129` | `f36b_0006` | `vix_zscore_20|vortex_indicator` | 1.089 | 7.366 | 7.364 | 1.058 | 8.252 | 8.615 | True | False | False |
| `f36c_0157` | `f36b_0016` | `vix_zscore_20|di_spread_14` | 1.074 | 7.585 | 9.580 | 1.110 | 8.443 | 9.487 | True | False | False |
| `f36c_0147` | `f36b_0194` | `di_spread_14|roc_12` | 1.085 | 8.781 | 13.797 | 1.135 | 9.336 | 8.832 | True | False | False |
| `f36c_0116` | `f36b_0033` | `vortex_indicator|rsi_14` | 1.056 | 7.596 | 8.234 | 1.176 | 7.931 | 5.677 | True | False | False |

Next action(다음 행동): `frontier36D_stage_closeout_short_source_utility_label_pivot_v1`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
