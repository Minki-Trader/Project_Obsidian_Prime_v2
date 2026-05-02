# run04B_mlp_input_geometry_runtime_handoff_probe_v1 Result Summary

- status(상태): `completed`
- judgment(판정): `inconclusive_input_geometry_runtime_handoff_probe_completed`
- no_trade_threshold(무거래 임계값): `1.01`
- boundary(경계): `runtime_handoff_probe_input_geometry_not_alpha_quality_not_promotion_not_runtime_authority`

## Input Geometry(입력 기하)

| split(분할) | mean_abs_z_max(최대 평균 z) | outlier_rate_max(최대 이상치 비율) |
|---|---:|---:|
| train | 1.738060185891861e-14 | 0.08849496954349463 |
| validation | 1.24152374148544 | 0.1292157659488013 |
| oos | 1.664429232106713 | 0.1909282700421941 |

## MT5 Handoff(MT5 인계)

| view(보기) | split(분할) | feature_ready(피처 준비) | model_ok(모델 정상) | trades(거래) |
|---|---:|---:|---:|---:|
| mt5_tier_a_handoff_validation_is | validation_is | 9844 | 9844 | 0 |
| mt5_tier_b_fallback_handoff_validation_is | validation_is | 2366 | 2366 | 0 |
| mt5_routed_total_validation_is | validation_is | 12210 | 12210 | 0 |
| mt5_tier_a_handoff_oos | oos | 7584 | 7584 | 0 |
| mt5_tier_b_fallback_handoff_oos | oos | 1062 | 1062 | 0 |
| mt5_routed_total_oos | oos | 8646 | 8646 | 0 |

효과(effect, 효과): 이 실행은 거래 성과가 아니라 입력 행렬과 MT5(메타트레이더5) 런타임 인계가 정상인지 보는 runtime_handoff_probe(런타임 인계 탐침)이다.
