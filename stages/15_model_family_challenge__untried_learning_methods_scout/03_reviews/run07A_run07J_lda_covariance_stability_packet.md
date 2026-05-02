# Stage15 LDA Covariance Stability Closeout(15단계 LDA 공분산 안정성 마감)

- judgment(판정): `closed_inconclusive_lda_covariance_stability_runtime_probe_evidence`
- completed runs(완료 실행): `10/10`
- MT5 KPI records(MT5 핵심성과지표 기록): `100`
- topic closeout(주제 마감): `lda_topic_closed_no_baseline_no_promotion`
- boundary(경계): `lda_covariance_stability_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`

| run(실행) | axis(축) | status(상태) | val net/trades(검증) | oos net/trades(표본외) | both+(동시 양수) |
|---|---|---:|---:|---:|---:|
| `run07A` | `eigen` `0.01` | `completed` | `-65.15/375` | `-123.6/246` | `False` |
| `run07B` | `eigen` `0.03` | `completed` | `129.07/386` | `-53.83/243` | `False` |
| `run07C` | `eigen` `0.05` | `completed` | `60.26/386` | `33.61/243` | `True` |
| `run07D` | `eigen` `0.08` | `completed` | `-59.7/389` | `-85.07/239` | `False` |
| `run07E` | `eigen` `0.12` | `completed` | `74.35/382` | `-124.57/243` | `False` |
| `run07F` | `eigen` `0.2` | `completed` | `-33.34/382` | `-100.41/237` | `False` |
| `run07G` | `lsqr` `0.03` | `completed` | `129.07/386` | `-53.83/243` | `False` |
| `run07H` | `lsqr` `0.05` | `completed` | `60.26/386` | `33.61/243` | `True` |
| `run07I` | `lsqr` `0.08` | `completed` | `-59.7/389` | `-85.07/239` | `False` |
| `run07J` | `eigen` `0.05` | `completed` | `60.26/386` | `33.61/243` | `True` |

- best OOS routed net(최고 표본외 라우팅 순수익): `run07C` `v13_eigen_shrinkage005` `33.61`
- best validation routed net(최고 검증 라우팅 순수익): `run07B` `v12_eigen_shrinkage003` `129.07`

효과(effect, 효과): LDA(선형 판별 분석)는 light eigen shrinkage(약한 고유값 수축) 주변에서 배울 단서가 있었지만, 이 결과는 edge(거래 우위), baseline(기준선), promotion(승격), runtime authority(런타임 권위)를 만들지 않는다.

다음 조건(next condition, 다음 조건): Stage15(15단계)는 LDA(선형 판별 분석) 소주제를 닫고 다음 untried learning method(미탐색 학습법)로 pivot(주제 전환)한다.
