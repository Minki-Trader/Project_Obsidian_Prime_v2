# Stage16 QDA RUN08A-RUN08J MT5 Runtime Probe(16단계 QDA 실행 08A-08J MT5 런타임 탐침)

- judgment(판정): `inconclusive_qda_characterization_mt5_runtime_probe_completed`
- completed runs(완료 실행): `10/10`
- MT5 KPI records(MT5 핵심성과지표 기록): `100`
- normalized KPI records(정규화 KPI 기록): `100`
- trade attribution records(거래 귀속 기록): `60`
- boundary(경계): `qda_characterization_mt5_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`

| run(실행) | topic(주제) | val net/trades(검증) | oos net/trades(표본외) |
|---|---|---:|---:|
| `run08A` | `near_raw_class_covariance_shape` | `52.68/331` | `181.69/291` |
| `run08B` | `class_prior_policy_shape` | `124.22/349` | `132.17/277` |
| `run08C` | `micro_regularization_floor` | `234.08/356` | `-39.92/275` |
| `run08D` | `light_regularization_shape` | `38.68/301` | `255.96/271` |
| `run08E` | `lda_shrinkage_anchor_transfer` | `-7.9/434` | `-23.01/285` |
| `run08F` | `moderate_regularization_shape` | `311.97/473` | `266.2/287` |
| `run08G` | `small_sample_covariance_fragility` | `79.23/355` | `221.89/253` |
| `run08H` | `larger_sample_covariance_stability` | `-156.72/350` | `86.67/245` |
| `run08I` | `core_feature_covariance_geometry` | `-130.08/236` | `-185.42/183` |
| `run08J` | `external_context_covariance_geometry` | `-41.31/509` | `-96.23/340` |

- best OOS routed net(최고 표본외 라우팅 순수익): `run08F` `moderate_regularization_shape` `266.2`

효과(effect, 효과): 이 묶음은 QDA(이차 판별 분석) 특성 파악 run(실행)을 MT5(메타트레이더5) Strategy Tester(전략 테스터), KPI(핵심성과지표), normalized KPI(정규화 KPI), trade attribution(거래 귀속)까지 연결한다.

금지 주장(forbidden claims, 금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).
