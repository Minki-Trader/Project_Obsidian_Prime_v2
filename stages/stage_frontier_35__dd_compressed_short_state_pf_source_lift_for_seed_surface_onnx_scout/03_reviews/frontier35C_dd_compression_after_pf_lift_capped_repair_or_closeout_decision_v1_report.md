# Frontier35C DD Repair After PF Lift Report(전선35C 수익 팩터 상승 후 손실폭 수리 보고서)

Updated(갱신): 2026-06-14T15:42:27Z

Status(상태): `dd_compression_after_pf_lift_capped_repair_closeout_queued_no_authority`

Judgment(판정): `dd_repair_after_pf_lift_collapsed_density_no_seed_runtime_requires_closeout`

Action(행동): F35B scout rows(전선35B 탐색 행)에 capped DD state repair(상한 손실폭 상태 수리)를 붙였습니다.

Effect(효과): PF lift(수익 팩터 상승)가 DD compression(손실폭 압축)을 견디며 5-10/day density(일 5-10회 밀도)를 유지하는지 확인합니다.

Candidate/scout/near-seed/seed/runtime rows(후보/탐색/근접 씨앗/씨앗/런타임 행): `4` / `0` / `0` / `0` / `0`

Best read-only candidate(최상 읽기 전용 후보): `f35c_0001`

Best validation PF-density-DD(최상 검증 수익 팩터-밀도-손실폭): `1.120` / `4.749/day` / `10.706%`

Best OOS PF-density-DD(최상 표본외 수익 팩터-밀도-손실폭): `1.272` / `5.122/day` / `7.414%`

Runtime probe status(런타임 탐침 상태): `runtime_probe_out_of_scope_by_claim_capped_repair_no_runtime_candidate`

| candidate(후보) | source(원천) | gate(게이트) | val PF | val density | val DD | OOS PF | OOS density | OOS DD | scout | near seed | seed |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `f35c_0001` | `f35b_0033` | `pf_lift:vix_zscore_20 >= q75 & dd_state:vortex_indicator <= q25` | 1.120 | 4.749 | 10.706 | 1.272 | 5.122 | 7.414 | False | False | False |
| `f35c_0002` | `f35b_0050` | `pf_lift:vortex_indicator <= q25 & dd_state:vix_zscore_20 >= q75` | 1.120 | 4.749 | 10.706 | 1.272 | 5.122 | 7.414 | False | False | False |
| `f35c_0003` | `f35b_0033` | `pf_lift:vix_zscore_20 >= q75 & dd_state:ema9_ema20_diff <= q25` | 1.128 | 4.923 | 10.147 | 1.190 | 5.267 | 8.342 | False | False | False |
| `f35c_0004` | `f35b_0033` | `pf_lift:vix_zscore_20 >= q75 & dd_state:close_ema50_ratio <= q25` | 1.051 | 4.503 | 15.027 | 1.147 | 4.802 | 9.269 | False | False | False |

Next action(다음 행동): `frontier35D_stage_closeout_pf_source_lift_v1`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
