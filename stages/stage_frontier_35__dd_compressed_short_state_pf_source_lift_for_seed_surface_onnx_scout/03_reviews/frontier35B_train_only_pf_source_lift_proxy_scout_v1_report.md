# Frontier35B PF Source Lift Proxy Report(전선35B 수익 팩터 원천 상승 프록시 보고서)

Updated(갱신): 2026-06-14T15:42:27Z

Status(상태): `train_only_pf_source_lift_proxy_scout_no_seed_no_runtime_candidate_no_authority`

Judgment(판정): `scout_clue_pf_lift_requires_dd_repair_or_closeout_no_authority`

Action(행동): F34 reference scaffold(F34 참조 발판)에서 short path-native candidates(숏 경로 기반 후보)에 train-only PF lift gate(학습 전용 수익 팩터 상승 게이트)를 붙였습니다.

Effect(효과): DD compression(손실폭 압축)이 아니라 PF source lift(수익 팩터 원천 상승)가 실제로 forward readout(전방 판독)을 올리는지 분리해 봅니다.

Candidate/scout/near-seed/seed/runtime rows(후보/탐색/근접 씨앗/씨앗/런타임 행): `62` / `21` / `1` / `0` / `0`

Best read-only candidate(최상 읽기 전용 후보): `f35b_0044`

Best validation PF-density-DD(최상 검증 수익 팩터-밀도-손실폭): `1.080` / `5.186/day` / `9.265%`

Best OOS PF-density-DD(최상 표본외 수익 팩터-밀도-손실폭): `1.344` / `5.282/day` / `9.476%`

Runtime probe status(런타임 탐침 상태): `runtime_probe_out_of_scope_by_claim_proxy_scout_only_no_runtime_candidate`

| candidate(후보) | source(원천) | gate(게이트) | val PF | val density | val DD | OOS PF | OOS density | OOS DD | scout | near seed | seed |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `f35b_0044` | `f33b_0176` | `pf_lift:ppo_hist_12_26_9 <= q25` | 1.080 | 5.186 | 9.265 | 1.344 | 5.282 | 9.476 | True | False | False |
| `f35b_0045` | `f33b_0176` | `pf_lift:close_ema20_ratio <= q25` | 1.125 | 6.667 | 10.556 | 1.269 | 6.901 | 7.826 | True | False | False |
| `f35b_0046` | `f33b_0176` | `pf_lift:adx_14 >= q60` | 1.159 | 5.858 | 11.673 | 1.255 | 5.885 | 7.529 | True | True | False |
| `f35b_0052` | `f33b_0171` | `pf_lift:ppo_hist_12_26_9 <= q25` | 1.093 | 5.339 | 12.266 | 1.374 | 5.580 | 7.913 | True | False | False |
| `f35b_0051` | `f33b_0172` | `pf_lift:ppo_hist_12_26_9 <= q25` | 1.093 | 5.339 | 12.266 | 1.374 | 5.580 | 7.913 | True | False | False |
| `f35b_0033` | `f33b_0176` | `pf_lift:vix_zscore_20 >= q75` | 1.120 | 5.328 | 10.948 | 1.235 | 5.656 | 8.280 | True | False | False |
| `f35b_0030` | `f33b_0172` | `pf_lift:di_spread_14 <= q15` | 1.109 | 6.180 | 13.006 | 1.285 | 6.137 | 6.070 | True | False | False |
| `f35b_0031` | `f33b_0171` | `pf_lift:di_spread_14 <= q15` | 1.109 | 6.180 | 13.006 | 1.285 | 6.137 | 6.070 | True | False | False |
| `f35b_0057` | `f33b_0176` | `pf_lift:roc_12 <= q25` | 1.103 | 6.180 | 11.660 | 1.229 | 6.405 | 9.356 | True | False | False |
| `f35b_0035` | `f33b_0176` | `pf_lift:vortex_indicator <= q15` | 1.100 | 5.366 | 13.749 | 1.375 | 5.275 | 8.700 | True | False | False |
| `f35b_0042` | `f33b_0176` | `pf_lift:rsi_14 <= q15` | 1.107 | 6.180 | 13.668 | 1.283 | 6.137 | 5.953 | True | False | False |
| `f35b_0041` | `f33b_0176` | `pf_lift:rsi_14_minus_50 <= q15` | 1.107 | 6.180 | 13.668 | 1.283 | 6.137 | 5.953 | True | False | False |

Next action(다음 행동): `frontier35C_dd_compression_after_pf_lift_capped_repair_or_closeout_decision_v1`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
