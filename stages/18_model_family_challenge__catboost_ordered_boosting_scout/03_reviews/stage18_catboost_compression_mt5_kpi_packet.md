# Stage18 CatBoost Compression MT5 KPI Batch(18단계 캣부스트 압축 MT5 KPI 배치)

- judgment(판정): `inconclusive_catboost_compression_mt5_kpi_completed`
- recommendation(권고): `close_or_downgrade_stage18_after_compression_unless_user_requests_more_exploration`
- boundary(경계): `runtime_probe_and_model_characteristic_compression_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`
- attempts(시도): `6`
- MT5 KPI records(MT5 KPI 기록): `18`

| run(실행) | topic(주제) | OOS net/PF/trades/DD(표본 밖 순손익/수익 팩터/거래/손실폭) |
|---|---|---:|
| `run12N` | `q85_high_margin_low_vol_mid_session_intersection` | `100.0 / 1.38 / 7 / 44.19` |
| `run12O` | `long_only_hold6_q85_compression` | `197.5 / 1.25 / 275 / 18.38` |
| `run12P` | `plain_control_same_condition_rematch` | `31.93 / 1.13 / 10 / 50.94` |

- ordered vs plain OOS net delta(Ordered-Plain 표본 밖 순손익 차이): `68.07`
- ordered vs plain OOS DD delta(Ordered-Plain 표본 밖 손실폭 차이): `-6.75`

효과(effect, 효과): 좋은 구간을 압축했을 때 CatBoost(`Categorical Boosting`, 범주형 부스팅/캣부스트) 특성이 위험 감소로 이어지는지, 그리고 Ordered boosting(순서형 부스팅) 고유성이 Plain boosting(Plain 부스팅) 대조군 앞에서도 남는지 확인했다.

금지 주장(forbidden claims, 금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).
