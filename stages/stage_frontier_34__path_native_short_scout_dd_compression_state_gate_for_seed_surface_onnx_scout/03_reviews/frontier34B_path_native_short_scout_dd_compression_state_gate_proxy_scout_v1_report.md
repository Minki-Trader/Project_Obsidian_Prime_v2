# Frontier34B DD Compression State Gate Proxy Scout Report(전선34B 손실폭 압축 상태 게이트 프록시 탐색 보고서)

Updated(갱신): 2026-06-14T15:01:22Z

Status(상태): `dd_compression_state_gate_proxy_scout_no_seed_no_runtime_candidate_no_authority`

Judgment(판정): `scout_clue_dd_compression_requires_capped_repair_or_closeout_no_authority`

Action(행동): F33-style short path-native replay(전선33식 숏 경로 기반 재생)에 train-only state gate(학습 전용 상태 게이트)를 붙였습니다.

Effect(효과): 검증/표본외는 읽기 전용으로 두고 DD compression(손실폭 압축)이 PF/density(수익 팩터/밀도)를 망가뜨리는지 확인합니다.

Candidate/scout/near-seed/seed/runtime rows(후보/탐색/근접 씨앗/씨앗/런타임 행): `242` / `56` / `1` / `0` / `0`

Best read-only candidate(최상 읽기 전용 후보): `f34b_0178`

Best validation PF-density-DD(최상 검증 수익 팩터-밀도-손실폭): `1.090` / `5.191/day` / `7.093%`

Best OOS PF-density-DD(최상 표본외 수익 팩터-밀도-손실폭): `1.195` / `5.099/day` / `6.025%`

Runtime probe status(런타임 탐침 상태): `runtime_probe_out_of_scope_by_claim_proxy_scout_only_no_runtime_candidate`

| candidate(후보) | source(원천) | gate(게이트) | val PF | val density | val DD | OOS PF | OOS density | OOS DD | scout | near seed | seed |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `f34b_0178` | `f33b_0176` | `vix_change_1 >= q60` | 1.090 | 5.191 | 7.093 | 1.195 | 5.099 | 6.025 | True | False | False |
| `f34b_0187` | `f33b_0176` | `gap_percent <= q40` | 1.119 | 5.273 | 9.422 | 1.281 | 5.130 | 6.019 | True | False | False |
| `f34b_0057` | `f33b_0176` | `ppo_hist_12_26_9 <= q25` | 1.080 | 5.186 | 9.265 | 1.344 | 5.282 | 9.476 | True | False | False |
| `f34b_0150` | `f33b_0176` | `ema9_ema20_diff <= q15` | 1.149 | 5.847 | 10.419 | 1.260 | 6.305 | 7.393 | True | False | False |
| `f34b_0095` | `f33b_0176` | `ema9_ema20_diff <= q25` | 1.140 | 7.033 | 9.941 | 1.237 | 7.069 | 7.694 | True | False | False |
| `f34b_0058` | `f33b_0176` | `close_ema20_ratio <= q25` | 1.125 | 6.667 | 10.556 | 1.269 | 6.901 | 7.826 | True | False | False |
| `f34b_0190` | `f33b_0171` | `gap_percent <= q40` | 1.073 | 5.093 | 10.242 | 1.263 | 5.511 | 6.405 | True | False | False |
| `f34b_0191` | `f33b_0172` | `gap_percent <= q40` | 1.073 | 5.093 | 10.242 | 1.263 | 5.511 | 6.405 | True | False | False |
| `f34b_0158` | `f33b_0176` | `us10yr_change_1 >= q60` | 1.074 | 5.087 | 11.388 | 1.279 | 5.221 | 5.513 | True | False | False |
| `f34b_0061` | `f33b_0176` | `adx_14 >= q60` | 1.159 | 5.858 | 11.673 | 1.255 | 5.885 | 7.529 | True | True | False |
| `f34b_0073` | `f33b_0171` | `ppo_hist_12_26_9 <= q25` | 1.093 | 5.339 | 12.266 | 1.374 | 5.580 | 7.913 | True | False | False |
| `f34b_0074` | `f33b_0172` | `ppo_hist_12_26_9 <= q25` | 1.093 | 5.339 | 12.266 | 1.374 | 5.580 | 7.913 | True | False | False |

Next action(다음 행동): `frontier34C_dd_compression_state_gate_capped_repair_or_closeout_decision_v1`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
