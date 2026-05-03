# Stage17 RUN11G XGBoost DART Attribution Closeout(17단계 실행11G XGBoost DART 귀속 마감)

- judgment(판정): `closed_inconclusive_xgboost_dart_attribution_no_new_axis_after_run11G`
- recommendation(권고): `close_stage17_after_dart_attribution_no_new_axis`
- feature shift(피처 변화): `is_first_30m_after_open=>close_ema20_ratio`
- long skew persisted(롱 편향 지속): `True`
- both splits positive(두 분할 모두 양수): `True`
- risk blocks quality claim(위험이 품질 주장 차단): `True`
- boundary(경계): `xgboost_dart_attribution_closeout_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`

| split(분할) | trades(거래 수) | avg hold(평균 보유) | long net(롱 순수익) | short net(숏 순수익) | positive months(양수 월 비율) |
|---|---:|---:|---:|---:|---:|
| `validation` | `291` | `43.4227` | `144.95` | `-19.78` | `0.444444` |
| `oos` | `259` | `25.749` | `125.77` | `67.46` | `0.714286` |

효과(effect, 효과): DART(`Dropouts meet Multiple Additive Regression Trees`, 드롭아웃 부스팅)는 새 피처 단서를 남겼지만, 거래 형태는 Stage17(17단계)의 기존 롱 편향을 벗어나지 않았다.

금지 주장(forbidden claims, 금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).
