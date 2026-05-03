# Stage16 QDA RUN08A-RUN08J Characterization(16단계 QDA 실행 08A-08J 특성 파악)

- judgment(판정): `inconclusive_qda_characterization_structural_scout_completed`
- completed runs(완료 실행): `10/10`
- MT5 KPI records(MT5 핵심성과지표 기록): `0`
- boundary(경계): `qda_characterization_structural_scout_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`

| run(실행) | topic(주제) | feature mode(피처 방식) | reg(정규화) | rows/class(클래스별 행) | shape(모양) | val/oos coverage(검증/표본외 비율) |
|---|---|---|---:|---:|---:|---:|
| `run08A` | `near_raw_class_covariance_shape` | `full58` | `0.001` | `600` | `0.922894` | `0.100061/0.146493` |
| `run08B` | `class_prior_policy_shape` | `full58` | `0.001` | `600` | `0.884004` | `0.100061/0.169172` |
| `run08C` | `micro_regularization_floor` | `full58` | `0.003` | `600` | `0.923868` | `0.100061/0.131857` |
| `run08D` | `light_regularization_shape` | `full58` | `0.01` | `600` | `0.871630` | `0.100061/0.155459` |
| `run08E` | `lda_shrinkage_anchor_transfer` | `full58` | `0.05` | `600` | `0.868841` | `0.100061/0.103639` |
| `run08F` | `moderate_regularization_shape` | `full58` | `0.15` | `600` | `0.891928` | `0.100061/0.079246` |
| `run08G` | `small_sample_covariance_fragility` | `full58` | `0.05` | `300` | `0.918027` | `0.100061/0.099947` |
| `run08H` | `larger_sample_covariance_stability` | `full58` | `0.05` | `1200` | `0.903961` | `0.100061/0.093354` |
| `run08I` | `core_feature_covariance_geometry` | `core42` | `0.05` | `600` | `0.941072` | `0.100061/0.084256` |
| `run08J` | `external_context_covariance_geometry` | `external16` | `0.05` | `600` | `0.950636` | `0.100061/0.073708` |

- highest shape score(최고 모양 점수): `run08J` `external_context_covariance_geometry` `0.9506362640451873`
- highest OOS signal coverage(최고 표본외 신호 비율): `run08B` `class_prior_policy_shape` `0.16917194092827004`

효과(effect, 효과): 이 묶음은 QDA(이차 판별 분석)의 class covariance(클래스별 공분산), prior(사전확률), regularization(정규화), sample size(표본 크기), feature geometry(피처 기하)를 수익 선택 없이 나란히 읽는다.

금지 주장(forbidden claims, 금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).
