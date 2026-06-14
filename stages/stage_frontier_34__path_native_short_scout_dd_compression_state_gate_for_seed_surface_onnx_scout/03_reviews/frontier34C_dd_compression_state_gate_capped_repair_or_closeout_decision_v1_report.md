# Frontier34C Capped Repair Report(전선34C 상한 수리 보고서)

Updated(갱신): 2026-06-14T15:01:22Z

Status(상태): `dd_compression_state_gate_capped_repair_scout_only_closeout_queued_no_authority`

Judgment(판정): `dd_compression_repair_preserved_clue_but_no_seed_runtime_requires_closeout`

Action(행동): F34B scout rows(전선34B 탐색 행)에 좁은 2단 state gate(2단 상태 게이트)를 상한 수리로 붙였습니다.

Effect(효과): DD(손실폭)는 더 눌렸지만 PF(수익 팩터)가 seed/runtime(씨앗/런타임)까지 올라가지 못하는지 확인합니다.

Candidate/scout/near-seed/seed/runtime rows(후보/탐색/근접 씨앗/씨앗/런타임 행): `222` / `99` / `6` / `0` / `0`

Best read-only candidate(최상 읽기 전용 후보): `f34c_0181`

Best validation PF-density-DD(최상 검증 수익 팩터-밀도-손실폭): `1.101` / `5.038/day` / `6.003%`

Best OOS PF-density-DD(최상 표본외 수익 팩터-밀도-손실폭): `1.189` / `5.015/day` / `6.025%`

Runtime probe status(런타임 탐침 상태): `runtime_probe_out_of_scope_by_claim_capped_repair_scout_only_no_runtime_candidate`

| candidate(후보) | source(원천) | gate(게이트) | val PF | val density | val DD | OOS PF | OOS density | OOS DD | scout | near seed | seed |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `f34c_0181` | `f34b_0178` | `vix_change_1 >= q60 & ema9_ema20_diff <= q40` | 1.101 | 5.038 | 6.003 | 1.189 | 5.015 | 6.025 | True | False | False |
| `f34c_0183` | `f34b_0178` | `vix_change_1 >= q60 & close_ema20_ratio <= q40` | 1.105 | 5.153 | 6.195 | 1.191 | 5.076 | 6.091 | True | False | False |
| `f34c_0185` | `f34b_0178` | `vix_change_1 >= q60 & close_ema50_ratio <= q40` | 1.115 | 5.098 | 5.946 | 1.161 | 5.008 | 6.296 | True | False | False |
| `f34c_0194` | `f34b_0187` | `gap_percent <= q40 & close_ema50_ratio <= q40` | 1.150 | 5.131 | 7.706 | 1.248 | 5.038 | 6.614 | True | True | False |
| `f34c_0170` | `f34b_0178` | `vix_change_1 >= q60 & bb_position_20 <= q40` | 1.095 | 5.180 | 6.790 | 1.194 | 5.076 | 6.217 | True | False | False |
| `f34c_0191` | `f34b_0187` | `gap_percent <= q40 & ema9_ema20_diff <= q40` | 1.131 | 5.137 | 8.445 | 1.260 | 5.053 | 5.941 | True | False | False |
| `f34c_0188` | `f34b_0187` | `gap_percent <= q40 & close_ema20_ratio <= q40` | 1.126 | 5.169 | 8.725 | 1.273 | 5.099 | 6.019 | True | False | False |
| `f34c_0037` | `f34b_0057` | `ppo_hist_12_26_9 <= q25 & close_ema50_ratio <= q40` | 1.095 | 5.120 | 8.560 | 1.321 | 5.206 | 9.476 | True | False | False |
| `f34c_0047` | `f34b_0057` | `ppo_hist_12_26_9 <= q25 & close_ema20_ratio <= q40` | 1.084 | 5.169 | 9.043 | 1.340 | 5.275 | 9.476 | True | False | False |
| `f34c_0036` | `f34b_0057` | `ppo_hist_12_26_9 <= q25 & ema9_ema20_diff <= q40` | 1.073 | 5.131 | 8.969 | 1.340 | 5.260 | 9.317 | True | False | False |
| `f34c_0051` | `f34b_0095` | `ema9_ema20_diff <= q25 & vortex_indicator <= q25` | 1.143 | 6.273 | 8.962 | 1.261 | 6.344 | 9.398 | True | False | False |
| `f34c_0041` | `f34b_0057` | `ppo_hist_12_26_9 <= q25 & vortex_indicator <= q40` | 1.071 | 5.158 | 9.248 | 1.350 | 5.275 | 9.476 | True | False | False |

Next action(다음 행동): `frontier34D_stage_closeout_dd_compression_state_gate_v1`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
