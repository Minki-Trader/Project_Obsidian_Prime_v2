# frontier02D ONNX Seed Repair Report(전선02D 온엑스 씨앗 수리 보고)

- run_id(실행 ID): `frontier02D_review_and_repair_onnx_seed_surface_v1`
- status(상태): `completed_onnx_seed_repair_scout_no_authority(온엑스 씨앗 수리 탐색 완료, 권위 없음)`
- trained_models(학습 모델 수): `2`
- ONNX parity pass(온엑스 동등성 통과): `2/2`
- decision_rows(결정 표면 행): `576`
- repair_observation_rows(수리 관찰 행): `14`

## Boundary(경계)

이번 실행(run, 실행)은 cheap ONNX repair scout(저비용 온엑스 수리 탐색)입니다. WFO(워크포워드), MT5 runtime validation(MT5 런타임 검증), baseline selection(기준선 선택), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 주장하지 않습니다.

## Best Validation Rank(검증 순위 1위)

- candidate_id(후보 ID): `f02d_ret_m1c_lr_c050__mid_cash__both__p34__m0__cd12`
- candidate_model_id(후보 모델 ID): `f02d_ret_m1c_lr_c050`
- label_id(라벨 ID): `ret_m1c`
- filter/side(필터/방향): `mid_cash` / `both`
- threshold/margin/cooldown(임계값/마진/쿨다운): `0.34` / `0` / `12`
- validation net/PF/density/DD(검증 순수익/수익 팩터/밀도/손실폭): `0.0905902` / `1.10035` / `3.19126` / `8.32627%`
- OOS net/PF/density/DD(표본외 순수익/수익 팩터/밀도/손실폭): `-0.00281852` / `0.995483` / `3.48092` / `9.4608%`
- joint_pass_count(동시 통과 수): validation(검증) `1`, OOS(표본외) `1`

## Read(판독)

Repair observation(수리 관찰)은 있습니다. 다만 PF(수익 팩터) 목표와 smoothness(매끄러움)가 여전히 약하면 다음 행동(action, 행동)은 수리 표면을 더 좁히거나 WFO/MT5(워크포워드/MT5) 전 Grok review(그록 검토)로 넘어갈지 판정하는 것입니다.

## Skipped Models(건너뛴 모델)

- none(없음)

## Artifacts(산출물)

- repair_model_training_summary: `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/02_runs/frontier02D_review_and_repair_onnx_seed_surface_v1/repair_model_training_summary.csv` sha256(해시) `8e100f5a58e8495026e353fdaaf1d934990cef8fbef3bccc8faecfc1889a5738`
- repair_classifier_metrics: `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/02_runs/frontier02D_review_and_repair_onnx_seed_surface_v1/repair_classifier_metrics.csv` sha256(해시) `250ad0ecf9d9f1d3502780fe6ddd6961c58a4c3227d41eee10401242a2105502`
- repair_decision_surface_metrics: `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/02_runs/frontier02D_review_and_repair_onnx_seed_surface_v1/repair_decision_surface_metrics.csv` sha256(해시) `997c175af9f7d839b480a0dc446f9817b79d31897072085ecf391b9566468d94`
- repair_decision_surface_summary: `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/02_runs/frontier02D_review_and_repair_onnx_seed_surface_v1/repair_decision_surface_summary.csv` sha256(해시) `1aa23a45839bf6f9aed7f9b269b28b34cc972eda6b3d6142a029c291220e75ed`
- top_repaired_onnx_seed_surfaces: `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/02_runs/frontier02D_review_and_repair_onnx_seed_surface_v1/top_repaired_onnx_seed_surfaces.csv` sha256(해시) `2a15c42b8b3b162ef545aa68f62d54f07b809f7c98667878203148ab28a9026e`
- top_repair_signal_replay: `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/02_runs/frontier02D_review_and_repair_onnx_seed_surface_v1/top_repair_signal_replay.csv` sha256(해시) `44651ec53b5d45ffd0c7cf254b6f7d7b35a6d94d947ce97deb416ca603e7efd3`
- repair_model_export_records: `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/02_runs/frontier02D_review_and_repair_onnx_seed_surface_v1/repair_model_export_records.json` sha256(해시) `1292880bf3c613733f9ede1eddcd31de2ff08431ea47f6bd59c40df937352cec`
- repair_onnx_parity_audit: `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/02_runs/frontier02D_review_and_repair_onnx_seed_surface_v1/repair_onnx_parity_audit.json` sha256(해시) `1e9f261b4971e5eca6147960df576d28f6e1870bdef0d47f822bcc653c07934a`
- repair_seed_surface_spec: `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/02_runs/frontier02D_review_and_repair_onnx_seed_surface_v1/repair_seed_surface_spec.json` sha256(해시) `bc356cb799ec50c25bdb1d6376f00ef51e51ed755312ef6fe181b85f03aeec43`
- input_integrity_audit: `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/02_runs/frontier02D_review_and_repair_onnx_seed_surface_v1/input_integrity_audit.json` sha256(해시) `fb59c89873d8f98589984325550d1417de4a86635aea29fe82a134dd214bb5d9`
- onnx_model__f02d_native_lr_c050: `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/02_runs/frontier02D_review_and_repair_onnx_seed_surface_v1/models/f02d_native_lr_c050.onnx` sha256(해시) `2496b1e9f1cdc456aa08f36829d400a7eb36c7fad9c4b2dfbe8e25141f9b9f92`
- onnx_model__f02d_ret_m1c_lr_c050: `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/02_runs/frontier02D_review_and_repair_onnx_seed_surface_v1/models/f02d_ret_m1c_lr_c050.onnx` sha256(해시) `6c35efb10d399b0b943bfc6ea1ac49276c65ff72ccd60951f9046b32f247087c`

## Gate Boundary(게이트 경계)

- Tier A separate(Tier A 분리): materialized(물질화)
- Tier B separate(Tier B 분리): partial-context Tier B artifact(부분 문맥 Tier B 산출물)를 만들지 않았으므로 `missing_required(필수 누락)`입니다.
- Tier A+B combined(Tier A+B 합산): routed Tier B fallback(라우팅 Tier B 대체)을 실행하지 않았으므로 `out_of_scope_by_claim(주장 범위 밖)`입니다.
- Grok pre-expensive review(비싼 검증 전 그록 검토): 이번 cheap repair scout(저비용 수리 탐색)에는 새 호출을 하지 않았고, WFO/MT5(워크포워드/MT5) 전에는 required(필요)입니다.
