# Frontier39B Regime Ablation Proxy Report(전선39B 체제 소거 프록시 보고)

Updated(갱신): 2026-06-14T18:22:45Z

Status(상태): `regime_conditioned_score_paired_ablation_complete_no_authority`

Judgment(판정): `ablation_guardrail_failed_despite_scout_surface`

Action(행동): A/B paired ablation(쌍대 소거)로 ungated score(무게이트 점수)와 same score + train-only regime gate(동일 점수 + 학습 전용 체제 게이트)를 비교했다.

Effect(효과): regime gate(체제 게이트)가 scout surface(탐색 표면)를 만들더라도 matched PF lift(동일 조건 수익 팩터 상승)가 없으면 다음 수리를 금지한다.

Candidate/scout/ablation-pass/seed/runtime rows(후보/탐색/소거 통과/씨앗/런타임 행): `335` / `335` / `0` / `0` / `0`

Best candidate(최상 후보): `f39b_0001`

Best B validation/OOS PF-density-DD(최상 B 검증/표본밖 수익 팩터-밀도-손실폭): `1.125` / `4.301` / `8.342` and `1.284` / `4.328` / `4.607`

Best min PF lift vs A(A 대비 최소 수익 팩터 상승): `0.032`

Runtime probe status(런타임 탐침 상태): `runtime_probe_out_of_scope_by_claim_proxy_no_seed_or_runtime_candidate`

| candidate(후보) | model(모델) | regime(체제) | B val PF | B val density | B val DD | B OOS PF | B OOS density | B OOS DD | min lift | ablation pass | seed |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `f39b_0001` | `logreg_C0.03` | `session_early_0_120` | 1.125 | 4.301 | 8.342 | 1.284 | 4.328 | 4.607 | 0.032 | False | False |
| `f39b_0002` | `logreg_C0.03` | `session_early_0_120` | 1.155 | 4.301 | 8.224 | 1.287 | 4.328 | 6.489 | 0.021 | False | False |
| `f39b_0003` | `logreg_C0.03` | `session_early_0_120` | 1.133 | 4.301 | 8.503 | 1.301 | 4.328 | 6.254 | 0.026 | False | False |
| `f39b_0004` | `extratrees_d4_leaf160` | `ema20_ema50_spread_zscore_50_low33` | 1.107 | 5.311 | 9.003 | 1.150 | 6.031 | 4.382 | 0.032 | False | False |
| `f39b_0005` | `extratrees_d4_leaf160` | `ema20_ema50_spread_zscore_50_low33` | 1.121 | 5.311 | 10.252 | 1.168 | 6.031 | 4.735 | 0.035 | False | False |
| `f39b_0006` | `extratrees_d4_leaf160` | `ema20_ema50_spread_zscore_50_low33` | 1.072 | 5.311 | 9.940 | 1.160 | 6.031 | 4.530 | 0.043 | False | False |
| `f39b_0007` | `extratrees_d4_leaf160` | `ema20_ema50_spread_zscore_50_low33` | 1.160 | 5.311 | 11.362 | 1.167 | 6.031 | 5.382 | 0.032 | False | False |
| `f39b_0008` | `extratrees_d4_leaf160` | `ema20_ema50_spread_zscore_50_low33` | 1.064 | 5.311 | 8.664 | 1.154 | 6.031 | 3.640 | 0.038 | False | False |
| `f39b_0009` | `logreg_C0.03` | `session_early_0_120` | 1.136 | 4.301 | 7.986 | 1.259 | 4.328 | 4.821 | 0.019 | False | False |
| `f39b_0010` | `extratrees_d4_leaf160` | `ema20_ema50_spread_zscore_50_low33` | 1.122 | 5.311 | 10.258 | 1.180 | 6.031 | 4.701 | 0.030 | False | False |
| `f39b_0011` | `extratrees_d4_leaf160` | `ema20_ema50_spread_zscore_50_low33` | 1.132 | 5.311 | 11.918 | 1.204 | 6.031 | 5.295 | 0.036 | False | False |
| `f39b_0012` | `extratrees_d4_leaf160` | `ema20_ema50_spread_zscore_50_low33` | 1.050 | 5.311 | 8.743 | 1.118 | 6.031 | 4.797 | 0.035 | False | False |

Next action(다음 행동): `frontier39C_regime_guardrail_closeout_decision_v1`
