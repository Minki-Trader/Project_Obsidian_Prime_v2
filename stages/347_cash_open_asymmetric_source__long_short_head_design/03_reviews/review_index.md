# Stage347 Review Index(347단계 검토 색인)

## Open From Stage346B(346B에서 개시)

- source_decision(원천 결정): `docs/decisions/2026-06-01_stage346B_cash_open_runtime_probe_source_pivot_review.md`
- current_run(현재 실행): `run347A_design_cash_open_asymmetric_long_short_source_without_db_v1`
- effect(효과): asymmetric long/short source design(비대칭 롱/숏 원천 설계)을 시작한다.

## run347A Cash-Open Asymmetric Source Design(347A 현금장 비대칭 원천 설계)

- report(보고서): `stages/347_cash_open_asymmetric_source__long_short_head_design/03_reviews/run347A_cash_open_asymmetric_source_design.md`
- final_decision(최종 결정): `stages/347_cash_open_asymmetric_source__long_short_head_design/02_runs/run347A/final_decision.json`
- next_run(다음 실행): `run347B_materialize_cash_open_asymmetric_source_inputs_without_db_v1`
- effect(효과): Stage347(347단계)의 비대칭 원천 설계를 물질화 대기열로 바꿨다.

## run347B Cash-Open Asymmetric Source Input Materialization(347B 현금장 비대칭 원천 입력 물질화)

- report(보고서): `stages/347_cash_open_asymmetric_source__long_short_head_design/03_reviews/run347B_cash_open_asymmetric_source_materialization.md`
- final_decision(최종 결정): `stages/347_cash_open_asymmetric_source__long_short_head_design/02_runs/run347B/final_decision.json`
- next_run(다음 실행): `run347C_train_cash_open_asymmetric_source_proxy_models_without_db_v1`
- effect(효과): teacher/source label(교사/원천 라벨)과 proxy grid(프록시 격자)를 물질화했다.

## run347C Cash-Open Asymmetric Source Proxy Training(347C 현금장 비대칭 원천 프록시 학습)

- report(보고서): `stages/347_cash_open_asymmetric_source__long_short_head_design/03_reviews/run347C_cash_open_asymmetric_source_proxy_training.md`
- final_decision(최종 결정): `stages/347_cash_open_asymmetric_source__long_short_head_design/02_runs/run347C/final_decision.json`
- next_run(다음 실행): `run347D_review_cash_open_asymmetric_source_proxy_training_without_db_v1`
- effect(효과): proxy model(프록시 모델), ONNX smoke(온엑스 점검), threshold screen(임계값 선별)을 검토 대기열로 넘긴다.

## run348A Proxy Review Branch(348A 프록시 검토 분기)

- from(출발): `347_cash_open_asymmetric_source__long_short_head_design` / `run347C_train_cash_open_asymmetric_source_proxy_models_without_db_v1`
- to(도착): `348_cash_open_proxy_review__long_oos_gap_short_carry_triage` / `run348B_review_cash_open_asymmetric_proxy_training_without_db_v1`
- effect(효과): Stage347(347단계)의 review(검토) 부담을 Stage348(348단계)로 분리했다.
