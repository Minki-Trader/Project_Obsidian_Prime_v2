# Frontier40B Raw Feature Pocket Proxy Report(전선40B 원천 피처 포켓 프록시 보고)

Updated(갱신): 2026-06-14T18:54:01Z

Status(상태): `raw_feature_state_pocket_proxy_complete_no_authority`

Judgment(판정): `scout_surface_only_no_seed_runtime`

Condition rows(조건 행): `30`

Candidate rows(후보 행): `521`

Scout/seed/runtime rows(탐색/씨앗/런타임 행): `181` / `0` / `0`

Best candidate(최상 후보): `f40b_0001`

Best validation/OOS PF-density-DD(최상 검증/표본외 수익 팩터-밀도-손실폭): `1.154` / `7.262` / `11.867` and `1.158` / `7.985` / `13.517`

Best lift vs density-matched A(최상 밀도 맞춤 A 대비 상승): `0.187`

Top rows(상위 행):

| candidate(후보) | kind(종류) | rule(규칙) | val PF | val density | val DD | OOS PF | OOS density | OOS DD | lift | scout | seed |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| `` | `pair_and` | `vix_zscore_20 >= q75 & ppo_hist_12_26_9 <= q25` | 1.154 | 7.262 | 11.867 | 1.158 | 7.985 | 13.517 | 0.187 | True | False |
| `` | `pair_and` | `vix_zscore_20 >= q75 & ppo_hist_12_26_9 <= q25` | 1.165 | 7.262 | 11.823 | 1.199 | 7.985 | 13.434 | 0.175 | True | False |
| `` | `pair_and` | `vix_zscore_20 >= q75 & ppo_hist_12_26_9 <= q25` | 1.139 | 7.262 | 11.022 | 1.141 | 7.985 | 12.509 | 0.170 | True | False |
| `` | `pair_and` | `vix_zscore_20 >= q75 & ppo_hist_12_26_9 <= q25` | 1.150 | 7.262 | 8.861 | 1.174 | 7.985 | 10.799 | 0.160 | True | False |
| `` | `pair_and` | `vix_zscore_20 >= q75 & ppo_hist_12_26_9 <= q25` | 1.141 | 7.262 | 8.774 | 1.209 | 7.985 | 10.714 | 0.152 | True | False |
| `` | `pair_and` | `vix_zscore_20 >= q75 & ppo_hist_12_26_9 <= q25` | 1.113 | 7.262 | 9.871 | 1.136 | 7.985 | 11.736 | 0.140 | True | False |
| `` | `pair_and` | `vix_zscore_20 >= q85 & ppo_hist_12_26_9 <= q25` | 1.171 | 4.907 | 9.683 | 1.256 | 5.290 | 9.509 | 0.222 | True | False |
| `` | `pair_and` | `vix_zscore_20 >= q75 & ppo_hist_12_26_9 <= q25` | 1.120 | 7.262 | 11.097 | 1.157 | 7.985 | 12.725 | 0.137 | True | False |

Effect(효과): raw feature pocket(원천 피처 포켓)은 scout clue(탐색 단서)를 만들었는지 확인하지만, seed/runtime(씨앗/런타임)은 별도 행 수로만 말한다.
