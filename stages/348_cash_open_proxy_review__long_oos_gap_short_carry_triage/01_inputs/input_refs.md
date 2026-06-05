# Stage348 Input References(348단계 입력 참조)

## Primary Inputs(주 입력)

- final_decision(최종 결정): `stages/347_cash_open_asymmetric_source__long_short_head_design/02_runs/run347C/final_decision.json`
- scorecard(점수표): `stages/347_cash_open_asymmetric_source__long_short_head_design/02_runs/run347C/model_training_scorecard.csv`
- probe_queue(탐침 대기열): `stages/347_cash_open_asymmetric_source__long_short_head_design/02_runs/run347C/probe_priority_queue.csv`
- model_manifest(모델 목록): `stages/347_cash_open_asymmetric_source__long_short_head_design/02_runs/run347C/model_artifact_manifest.csv`
- onnx_smoke(온엑스 점검): `stages/347_cash_open_asymmetric_source__long_short_head_design/02_runs/run347C/onnx_parity_smoke.csv`

## Branch Outputs(분기 출력)

- branch_handoff(분기 인계): `stages/348_cash_open_proxy_review__long_oos_gap_short_carry_triage/02_runs/run348A/stage347_to_stage348_branch_handoff.csv`
- compact_score_summary(경량 점수 요약): `stages/348_cash_open_proxy_review__long_oos_gap_short_carry_triage/02_runs/run348A/run347C_compact_score_summary.csv`
- review_seed_surface(검토 씨앗 표면): `stages/348_cash_open_proxy_review__long_oos_gap_short_carry_triage/02_runs/run348A/stage348_review_seed_surface.csv`
- negative_memory_seed(부정 기억 씨앗): `stages/348_cash_open_proxy_review__long_oos_gap_short_carry_triage/02_runs/run348A/stage348_negative_memory_seed.csv`
- review_queue(검토 대기열): `stages/348_cash_open_proxy_review__long_oos_gap_short_carry_triage/02_runs/run348A/run348B_review_queue.csv`

Effect(효과): Stage348(348단계)은 Stage347(347단계)의 무거운 학습 산출물을 재생산하지 않고 필요한 표만 읽는다.
