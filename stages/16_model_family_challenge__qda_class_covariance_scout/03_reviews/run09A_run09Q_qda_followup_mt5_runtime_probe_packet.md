# Stage16 QDA RUN09A-RUN09Q Follow-up MT5 Runtime Probe(16단계 QDA 실행 09A-09Q 후속 MT5 런타임 탐침)

- judgment(판정): `inconclusive_qda_run09_followup_mt5_runtime_probe_completed`
- completed runs(완료 실행): `17/17`
- MT5 KPI records(MT5 핵심성과지표 기록): `170`
- normalized KPI records(정규화 KPI 기록): `170`
- trade attribution records(거래 귀속 기록): `102`
- baseline comparison(비교 기준): `run08F_qda_moderate_regularization150_characterization_v1`
- boundary(경계): `qda_run09_followup_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`

| run(실행) | axis(축) | topic(주제) | reg(정규화) | rows(행/클래스) | q(분위수) | features(피처) | val net/PF/trades(검증) | oos net/PF/trades(표본외) |
|---|---|---|---:|---:|---:|---:|---:|---:|
| `run09A` | `regularization` | `reg008_fine_search` | `0.08` | `600` | `0.9` | `58` | `-31.21/0.98/366` | `78.39/1.07/262` |
| `run09B` | `regularization` | `reg010_fine_search` | `0.1` | `600` | `0.9` | `58` | `-4.93/1.0/361` | `115.53/1.1/263` |
| `run09C` | `regularization` | `reg012_fine_search` | `0.12` | `600` | `0.9` | `58` | `178.93/1.12/342` | `269.83/1.3/217` |
| `run09D` | `regularization` | `reg018_fine_search` | `0.18` | `600` | `0.9` | `58` | `40.18/1.02/369` | `438.78/1.48/251` |
| `run09E` | `regularization` | `reg025_fine_search` | `0.25` | `600` | `0.9` | `58` | `-136.59/0.92/336` | `87.01/1.08/255` |
| `run09F` | `feature_removal` | `drop_macro6` | `0.15` | `600` | `0.9` | `52` | `128.95/1.09/315` | `-296.87/0.78/248` |
| `run09G` | `feature_removal` | `drop_mega10` | `0.15` | `600` | `0.9` | `48` | `118.99/1.11/216` | `432.81/1.63/173` |
| `run09H` | `feature_removal` | `drop_volatility9` | `0.15` | `600` | `0.9` | `49` | `69.7/1.04/421` | `60.05/1.05/311` |
| `run09I` | `feature_removal` | `drop_momentum12` | `0.15` | `600` | `0.9` | `46` | `-213.08/0.89/397` | `411.23/1.4/257` |
| `run09J` | `feature_removal` | `drop_session4` | `0.15` | `600` | `0.9` | `54` | `138.05/1.08/342` | `35.89/1.03/260` |
| `run09K` | `sample_size` | `sample300_reg015` | `0.15` | `300` | `0.9` | `58` | `-494.66/0.74/324` | `-382.88/0.74/268` |
| `run09L` | `sample_size` | `sample450_reg015` | `0.15` | `450` | `0.9` | `58` | `-202.69/0.9/376` | `109.21/1.09/281` |
| `run09M` | `sample_size` | `sample600_resample_reg015` | `0.15` | `600` | `0.9` | `58` | `28.66/1.02/385` | `-81.82/0.93/257` |
| `run09N` | `sample_size` | `sample900_reg015` | `0.15` | `900` | `0.9` | `58` | `-316.4/0.83/417` | `-149.52/0.88/293` |
| `run09O` | `coverage_threshold` | `coverage_q85` | `0.15` | `600` | `0.85` | `58` | `146.76/1.06/643` | `241.26/1.17/395` |
| `run09P` | `coverage_threshold` | `coverage_q93` | `0.15` | `600` | `0.93` | `58` | `220.81/1.14/364` | `121.63/1.14/202` |
| `run09Q` | `coverage_threshold` | `coverage_q95` | `0.15` | `600` | `0.95` | `58` | `23.62/1.02/292` | `75.54/1.1/161` |

- best OOS routed net(최고 표본외 라우팅 순수익): `run09D` `reg018_fine_search` `438.78`

효과(effect, 효과): 이 묶음은 QDA(이차판별분석) run08F 주변의 정규화, 피처 제거, 표본 크기, coverage threshold(커버리지 임계값)를 수익 최적화 없이 MT5(메타트레이더5) KPI(핵심성과지표)까지 비교한다.

금지 주장(forbidden claims, 금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).
