# Stage15 LDA RUN06A-RUN06J Runtime Probe(15단계 LDA 실행 06A-06J 런타임 탐침)

- judgment(판정): `inconclusive_lda_run06A_run06J_runtime_probe_completed`
- completed runs(완료 실행): `10/10`
- MT5 KPI records(MT5 KPI 기록): `100`
- boundary(경계): `lda_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`

| run(실행) | feature(특징) | status(상태) | shape(모양) | val net/trades(검증) | oos net/trades(표본외) |
|---|---|---:|---:|---:|---:|
| `run06A` | `svd_empirical_prior_geometry` | `completed` | `0.978965` | `-147.49/307` | `-172.77/235` |
| `run06B` | `prior_sensitivity` | `completed` | `0.978210` | `-3.71/217` | `-8.03/187` |
| `run06C` | `rank_tolerance_sensitivity` | `completed` | `0.982287` | `-281.91/286` | `-132.34/226` |
| `run06D` | `least_squares_covariance_raw` | `completed` | `0.956359` | `-44.8/247` | `41.45/230` |
| `run06E` | `least_squares_auto_shrinkage` | `completed` | `0.953894` | `-83.6/348` | `239.02/235` |
| `run06F` | `least_squares_light_shrinkage` | `completed` | `0.984659` | `-25.58/325` | `88.8/240` |
| `run06G` | `least_squares_heavy_shrinkage` | `completed` | `0.980899` | `-26.0/252` | `339.36/184` |
| `run06H` | `eigen_light_shrinkage` | `completed` | `0.945328` | `324.28/303` | `449.46/181` |
| `run06I` | `eigen_auto_shrinkage` | `completed` | `0.986807` | `200.57/265` | `-343.06/195` |
| `run06J` | `eigen_prior_and_shrinkage_combo` | `completed` | `0.980760` | `204.68/356` | `109.49/267` |

효과(effect, 효과): 이 표는 LDA(선형 판별 분석)의 solver(풀이 방식), shrinkage(공분산 축소), prior(사전확률), rank tolerance(랭크 허용치) 축을 수익 선택 없이 나란히 본 것이다.

금지 주장(forbidden claims, 금지 주장): alpha quality(알파 품질), edge(거래 우위), baseline(기준선), promotion(승격), runtime authority(런타임 권위).
