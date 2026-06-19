# Decision: Stage 337IA Training Review

- date: `2026-06-01`
- run_id: `run337IA_review_proxy_negative_trade_shape_offensive_pivot_training_without_db_v1`
- decision: `stage337IA_open_run337IB_materialize_proxy_positive_runtime_probe_package`
- judgment: `two_proxy_positive_onnx_candidates_found_short_dominant_side_risk_runtime_probe_required`
- next_run_id: `run337IB_materialize_proxy_positive_offensive_pivot_runtime_probe_package_without_db_v1`

## Reason

HZ training(학습)은 ONNX parity(ONNX 동등성) `7/7`을 통과했고, proxy-positive(프록시 양수) 후보 2개를 만들었다.

## Effect

proxy expected value(프록시 예상값)를 MT5 runtime probe(MT5 런타임 탐침)와 비교하기 위해 IB package(패키지)를 연다.

## Boundary

`research_development_training_review_only_no_candidate_selection_no_mt5_execution_in_IA_no_runtime_package_authority_no_forward_no_operating_or_goal_claim`
