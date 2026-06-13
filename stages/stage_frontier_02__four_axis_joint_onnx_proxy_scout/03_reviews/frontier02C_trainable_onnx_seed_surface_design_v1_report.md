# frontier02C Trainable ONNX Seed Surface Report(전선02C 학습 가능 온엑스 씨앗 표면 보고)

- run_id(실행 ID): `frontier02C_trainable_onnx_seed_surface_design_v1`
- status(상태): `completed_trainable_onnx_seed_surface_smoke_no_authority(학습 가능 온엑스 씨앗 표면 스모크 완료, 권위 없음)`
- trained_models(학습 모델 수): `6`
- ONNX parity pass(온엑스 동등성 통과): `6/6`
- decision_rows(결정 표면 행): `576`
- onnx_seed_observation_rows(온엑스 씨앗 관찰 행): `311`

## Boundary(경계)

이번 실행(run, 실행)은 proxy teacher(프록시 교사)를 3-class LogisticRegression(3클래스 로지스틱 회귀) ONNX(온엑스)로 내보내는 smoke training(스모크 학습)입니다. WFO(워크포워드), MT5 runtime validation(MT5 런타임 검증), baseline selection(기준선 선택), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 주장하지 않습니다.

## Best Validation Rank(검증 순위 1위)

- candidate_id(후보 ID): `frontier02c_logreg_teacher__trend_follow_joint__mid_cash__both__q70__cd6__p34__m0__cd6`
- candidate_model_id(후보 모델 ID): `frontier02c_logreg_teacher__trend_follow_joint__mid_cash__both__q70__cd6`
- teacher_candidate_id(교사 후보 ID): `trend_follow_joint__mid_cash__both__q70__cd6`
- threshold/margin/cooldown(임계값/마진/쿨다운): `0.34` / `0` / `6`
- validation net/PF/density/DD(검증 순수익/수익 팩터/밀도/손실폭): `0.236314` / `1.2034` / `4.29508` / `9.88436%`
- OOS net/PF/density/DD(표본외 순수익/수익 팩터/밀도/손실폭): `0.0464936` / `1.05433` / `5.03053` / `10.3356%`
- joint_pass_count(동시 통과 수): validation(검증) `1`, OOS(표본외) `1`

## Read(판독)

ONNX seed observation(온엑스 씨앗 관찰)은 있습니다. 다만 PF(수익 팩터)와 density(밀도)가 final target(최종 목표)에 아직 못 미치므로 repair/review(수리/검토)로 넘깁니다.

## Skipped Teachers(건너뛴 교사 표면)

- `macro_confirmation_joint__all_cash__long_only__q70__cd6`: `skipped_missing_train_label_class`
- `macro_confirmation_joint__mid_cash__long_only__q75__cd18`: `skipped_missing_train_label_class`

## Artifacts(산출물)

- model_training_summary: `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/02_runs/frontier02C_trainable_onnx_seed_surface_design_v1/model_training_summary.csv` sha256(해시) `92492672648f08af9da7f92b9971c5b67ddff34031c8a04d74677295f74f33c1`
- teacher_signal_audit: `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/02_runs/frontier02C_trainable_onnx_seed_surface_design_v1/teacher_signal_audit.csv` sha256(해시) `392cb809b00088dcbbf9f9425bfa5bda161115a55065ff1417a671dd548716f3`
- classifier_metrics: `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/02_runs/frontier02C_trainable_onnx_seed_surface_design_v1/classifier_metrics.csv` sha256(해시) `d848207a6a296b5991738b1b51d9866418e084229856fa887909e1164273bbe6`
- decision_surface_metrics: `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/02_runs/frontier02C_trainable_onnx_seed_surface_design_v1/decision_surface_metrics.csv` sha256(해시) `ebfd020bcb283da546754b433a20a6b099e9d1a5749208394a482c541e7eb73a`
- decision_surface_summary: `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/02_runs/frontier02C_trainable_onnx_seed_surface_design_v1/decision_surface_summary.csv` sha256(해시) `38946e3c8781261d29ab0e3c3aa3d5f51dec8ecdb3ddfdd5f25ed4858e790d8c`
- top_onnx_seed_surfaces: `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/02_runs/frontier02C_trainable_onnx_seed_surface_design_v1/top_onnx_seed_surfaces.csv` sha256(해시) `498f33ba13323922a5c01bd47dc85332583fbe7ed75a68b9b93eec15079a114a`
- top_decision_signal_replay: `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/02_runs/frontier02C_trainable_onnx_seed_surface_design_v1/top_decision_signal_replay.csv` sha256(해시) `f1077d8a96839583336ccb017cb4e7cb074730e5a6a07ba671a3d0f9ebded4ab`
- model_export_records: `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/02_runs/frontier02C_trainable_onnx_seed_surface_design_v1/model_export_records.json` sha256(해시) `6882157f75accfc0fe249cb9cbab7e1217b1eafd3c7dd2fc76a66f5ebcf6910e`
- onnx_parity_audit: `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/02_runs/frontier02C_trainable_onnx_seed_surface_design_v1/onnx_parity_audit.json` sha256(해시) `486dc2b7863019ff785d96a56c1002ea9d3223de4fa675755d0ff32f82648960`
- trainable_seed_surface_spec: `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/02_runs/frontier02C_trainable_onnx_seed_surface_design_v1/trainable_seed_surface_spec.json` sha256(해시) `1e3a240b3ee776f9b62ff10703e51f61b2548adcd8df239775f3953f1237cc9d`
- input_integrity_audit: `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/02_runs/frontier02C_trainable_onnx_seed_surface_design_v1/input_integrity_audit.json` sha256(해시) `948a3da191057d6735aca28afc7a8cb1427d12c2904b62ceaa883d7d8370f507`
- onnx_model__frontier02c_logreg_teacher__trend_follow_joint__all_cash__both__q70__cd6: `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/02_runs/frontier02C_trainable_onnx_seed_surface_design_v1/models/frontier02c_logreg_teacher__trend_follow_joint__all_cash__both__q70__cd6.onnx` sha256(해시) `79d5458222cf5c26ad84362a385cf38ed2296f3b2bd1cfcbbe11e7777c70a49c`
- onnx_model__frontier02c_logreg_teacher__macro_confirmation_joint__normal_vol__both__q70__cd6: `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/02_runs/frontier02C_trainable_onnx_seed_surface_design_v1/models/frontier02c_logreg_teacher__macro_confirmation_joint__normal_vol__both__q70__cd6.onnx` sha256(해시) `d757bce65cf6eb4b1d4599945528bf923d837555f806a952f2de3b2e25b39c4e`
- onnx_model__frontier02c_logreg_teacher__squeeze_breakout_joint__mid_cash__both__q75__cd6: `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/02_runs/frontier02C_trainable_onnx_seed_surface_design_v1/models/frontier02c_logreg_teacher__squeeze_breakout_joint__mid_cash__both__q75__cd6.onnx` sha256(해시) `4374052583d3aa09f938190fece5a615eded46bac8c1cd54b607ac21e31c132a`
- onnx_model__frontier02c_logreg_teacher__macro_confirmation_joint__mid_cash__both__q70__cd18: `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/02_runs/frontier02C_trainable_onnx_seed_surface_design_v1/models/frontier02c_logreg_teacher__macro_confirmation_joint__mid_cash__both__q70__cd18.onnx` sha256(해시) `14a629d6e85eca8ba444bda50cdcb9a10231c0a82478b1dcf800af750ed1dd1a`
- onnx_model__frontier02c_logreg_teacher__macro_confirmation_joint__mid_cash__both__q75__cd18: `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/02_runs/frontier02C_trainable_onnx_seed_surface_design_v1/models/frontier02c_logreg_teacher__macro_confirmation_joint__mid_cash__both__q75__cd18.onnx` sha256(해시) `6ccf47d7c5fefdf61a9423d5ca370608894d66af581c250b4ac357dd44bf7f90`
- onnx_model__frontier02c_logreg_teacher__trend_follow_joint__mid_cash__both__q70__cd6: `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/02_runs/frontier02C_trainable_onnx_seed_surface_design_v1/models/frontier02c_logreg_teacher__trend_follow_joint__mid_cash__both__q70__cd6.onnx` sha256(해시) `ffa54e957ee310096183acf618a2b1fe98fde4ebac824314506c06761cdd4e69`

## Gate Boundary(게이트 경계)

- Tier A separate(Tier A 분리): materialized(물질화)
- Tier B separate(Tier B 분리): partial-context Tier B artifact(부분 문맥 Tier B 산출물)를 만들지 않았으므로 `missing_required(필수 누락)`입니다.
- Tier A+B combined(Tier A+B 합산): routed Tier B fallback(라우팅 Tier B 대체)을 실행하지 않았으므로 `out_of_scope_by_claim(주장 범위 밖)`입니다.
- Grok pre-expensive review(비싼 검증 전 그록 검토): 이번 cheap ONNX smoke(저비용 온엑스 스모크)에는 새 호출을 하지 않았고, WFO/MT5(워크포워드/MT5) 전에는 required(필요)입니다.
