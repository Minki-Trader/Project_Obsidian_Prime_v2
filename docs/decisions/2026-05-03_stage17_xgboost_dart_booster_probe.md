# 2026-05-03 Stage17 XGBoost DART Booster Probe(17단계 XGBoost DART 부스터 탐침)

## Decision(결정)

`run11F_xgb_dart_booster_probe_v1`를 DART(`Dropouts meet Multiple Additive Regression Trees`, 드롭아웃 부스팅) 내부 부스터 탐침으로 실행했다.

효과(effect, 효과): 기존 gbtree(기본 트리 부스팅)에서 반복된 피처 동인과 롱 편향이 DART에서도 같은지 확인한다.

## Judgment(판정)

- judgment(판정): `inconclusive_xgboost_dart_booster_runtime_probe_completed`
- recommendation(권고): `keep_stage17_open_for_dart_followup_attribution`
- boundary(경계): `xgboost_dart_booster_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`
