# F80C WFO-Aware Surface Selection Report(F80C 워크포워드 인식 표면 선택 보고서)

Updated(갱신): 2026-06-17T15:33:53Z

- run id(실행 ID): `frontier80C_wfo_aware_surface_selection_v1`
- parent run(부모 실행): `frontier80B_broad_extreme_multi_axis_proxy_scout_v1`
- status(상태): `f80c_wfo_exportable_target_selected_for_mt5_materialization_no_authority`
- judgment(판정): `wfo_aware_materialization_target_selected_no_baseline_no_authority`
- claim boundary(주장 경계): `wfo_selection_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve_no_parity_only_economics`
- target candidate(대상 후보): `f80b_13315`
- target model(대상 모델): `extra_trees_d6_l120`
- target reason(대상 사유): `wfo_exportable_materialization_target(워크포워드 인식 내보내기 가능 물질화 대상)`

## Important Boundary(중요 경계)

Action(행동): F80B(전선80B)의 material proxy candidates(물질 프록시 후보)를 WFO-aware period stability(워크포워드 인식 기간 안정성)와 ONNX export feasibility(온엑스 내보내기 가능성)로 좁혔다.

Effect(효과): 이 대상은 MT5 materialization target(MT5 물질화 대상)일 뿐 selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위)가 아니다.

## Ranked Exportable Candidates(상위 내보내기 가능 후보)

| candidate(후보) | model(모델) | surface(표면) | feature(피처) | val/oos period+(검증/표본외 양수기간) | val KPI(검증) | OOS KPI(표본외) | export(내보내기) | gate(게이트) |
|---|---|---|---|---:|---:|---:|---|---:|
| `f80b_13315` | `extra_trees_d6_l120` | `order_intent_swing` | `micro_reversal` | `0.571/0.833` | `89.72893373785989/1.3786494266857832/4.056337901607913/396` | `65.20159991431154/1.4454005575081805/3.2467735467534564/252` | `export_ok` | `1` |
| `f80b_13318` | `extra_trees_d6_l120` | `order_intent_swing` | `micro_reversal` | `0.571/0.833` | `89.72893373785989/1.3786494266857832/4.056337901607913/396` | `65.20159991431154/1.4454005575081805/3.2467735467534564/252` | `export_ok` | `1` |
| `f80b_11410` | `histgbm_shallow` | `order_intent_swing` | `runtime_fill_context` | `0.778/1.000` | `127.59553909761912/1.4067444326617182/4.057224998205379/529` | `114.8630416340801/1.3902940422902441/3.3248380473311503/498` | `export_failed` | `0` |
| `f80b_11470` | `histgbm_shallow` | `order_intent_swing` | `runtime_fill_context` | `0.778/1.000` | `127.59553909761912/1.4067444326617182/4.057224998205379/529` | `114.8630416340801/1.3902940422902441/3.3248380473311503/498` | `export_failed` | `0` |
| `f80b_15010` | `histgbm_shallow` | `order_intent_swing` | `compact_exportable_28` | `0.778/1.000` | `127.59553909761912/1.4067444326617182/4.057224998205379/529` | `114.8630416340801/1.3902940422902441/3.3248380473311503/498` | `export_failed` | `0` |
| `f80b_15070` | `histgbm_shallow` | `order_intent_swing` | `compact_exportable_28` | `0.778/1.000` | `127.59553909761912/1.4067444326617182/4.057224998205379/529` | `114.8630416340801/1.3902940422902441/3.3248380473311503/498` | `export_failed` | `0` |
| `f80b_11473` | `histgbm_shallow` | `order_intent_swing` | `runtime_fill_context` | `0.778/0.857` | `120.8358630248701/1.354611129189717/4.057224998205379/565` | `128.87029690818866/1.4006895505509505/3.3248380473311503/546` | `export_failed` | `0` |
| `f80b_15073` | `histgbm_shallow` | `order_intent_swing` | `compact_exportable_28` | `0.778/0.857` | `120.8358630248701/1.354611129189717/4.057224998205379/565` | `128.87029690818866/1.4006895505509505/3.3248380473311503/546` | `export_failed` | `0` |
| `f80b_13481` | `histgbm_shallow` | `order_intent_swing` | `micro_reversal` | `0.667/1.000` | `99.65022208400492/1.4953893374846203/3.3180961131903586/349` | `60.185068655598194/1.3728669176444723/2.8812897485943494/272` | `export_failed` | `0` |
| `f80b_12193` | `histgbm_shallow` | `order_intent_swing` | `price_vol_session` | `0.625/1.000` | `120.7276372399783/1.4341569234204776/3.0941929319880046/473` | `83.64433817578822/1.3717180477804933/3.2467735467534564/379` | `export_failed` | `0` |

## Next Run(다음 실행)

`frontier80D_mt5_runtime_probe_quality_v1`
