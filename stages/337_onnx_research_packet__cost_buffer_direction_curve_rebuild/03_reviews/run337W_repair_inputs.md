# Stage337W Materialized Repair Inputs(337W 수리 입력 물질화)

- run_id(실행 ID): `run337W_materialize_cost_buffer_source_policy_repair_inputs_v1`
- status(상태): `completed_stage337W_cost_buffer_source_policy_repair_inputs_materialized_no_training_no_mt5`
- judgment(판정): `source_policy_cost_buffer_overfit_parity_inputs_materialized_no_onnx_or_forward_decision`
- decision(결정): `stage337W_open_run337X_review_materialized_repair_inputs_no_selection`
- parent_run(부모 실행): `run337V_cost_buffer_rebuild_and_source_policy_repair_design_v1`
- next_action(다음 행동): `run337X_review_materialized_cost_buffer_source_policy_repair_inputs_v1`
- selected_candidate(선택 후보): `none`
- model training(모델 학습): `not_run`
- MT5 execution(MT5 실행): `not_run`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## What Was Materialized(무엇을 물질화했나)

- source age rows(원천 나이 행): `8`
- feature boundary rows(피처 경계 행): `3`
- source repair decision rows(원천 수리 결정 행): `3`
- branch specs(분기 명세): `4`
- cost ladder rows(비용 사다리 행): `18`
- direction/curve gate rows(방향/곡선 게이트 행): `9`
- proxy expected rows(프록시 예상값 행): `3`
- proxy-MT5 schema rows(프록시-MT5 스키마 행): `11`
- usability rules(활용성 규칙): `4`
- tester boundary rows(테스터 경계 행): `1`
- model firewall rows(모델 방화벽 행): `8`
- gate audit rows(게이트 감사 행): `13`

## Read(판독)

run337W(337W 실행)는 run337V(337V 실행)의 설계를 실제 CSV/JSON 입력으로 바꿨다. 효과(effect, 효과)는 다음 run337X(337X 실행)가 source age audit(원천 나이 감사), feature-label boundary(피처-라벨 경계), proxy-MT5 difference(프록시-MT5 차이), tester feature_last reach(테스터 피처 끝 도달), cost/curve/direction gate(비용/곡선/방향 게이트)를 빠뜨렸는지 바로 검토할 수 있게 하는 것이다.

이번 실행은 수익 개선이나 후보 선택이 아니다. model training(모델 학습), threshold retuning(임계값 재조정), lot optimization(랏 최적화), MT5 runtime probe(MT5 런타임 탐침), Forward Passed/Failed(전진 통과/실패), operating promotion(운영 승격), Goal Achieve(목표 달성)는 모두 주장하지 않는다.
