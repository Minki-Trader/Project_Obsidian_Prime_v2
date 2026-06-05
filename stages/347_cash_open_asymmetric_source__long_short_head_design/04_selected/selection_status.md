# Stage 347 Selection Status(347단계 선정 상태)

- active_stage_at_handoff(인계 당시 단계): `347_cash_open_asymmetric_source__long_short_head_design`
- latest_completed_run(최근 완료 실행): `run347C_train_cash_open_asymmetric_source_proxy_models_without_db_v1`
- branched_to_stage(분기된 단계): `348_cash_open_proxy_review__long_oos_gap_short_carry_triage`
- branch_run(분기 실행): `run348A_branch_stage347_to_cash_open_proxy_review_without_db_v1`
- next_active_run(다음 활성 실행): `run348B_review_cash_open_asymmetric_proxy_training_without_db_v1`
- superseded_planned_run(대체된 예정 실행): `run347D_review_cash_open_asymmetric_source_proxy_training_without_db_v1`
- selected_model(선정 모델): `none(없음)`
- trained_model_artifacts(학습 모델 산출물): `9`
- onnx_allocator_smoke_passes(온엑스 배분기 점검 통과): `2`
- long_oos_status(롱 표본외 상태): `missing_positive_labels(양성 라벨 없음)`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): Stage347(347단계)은 proxy training/screen(프록시 학습/선별) 산출물을 보존하고, review(검토)는 Stage348(348단계)로 넘겼다.
