# run364ER OOS108 cost/side model-label-feature reseed(OOS108 비용/방향 모델-라벨-피처 재시드)

Created(생성): 2026-06-06T17:28:18Z

## Summary(요약)

Action(행동): EQ strict pass 0(엄격 통과 0)을 받아 cost-aware 3-class labels(비용 인식 3분류 라벨), regime/behavior features(국면/현상 피처), side-quality filters(방향 품질 필터)로 새 모델을 학습했습니다.

Effect(효과): 기존 EL surface(EL 표면) 미세조정 반복을 멈추고, 비용을 이긴 움직임만 더 강하게 학습하는 새 수익 원천을 열었습니다.

## Selected(선택)

- selected_model_id(선택 모델 ID): `costside_dir_h2_m3__costside_all72__et8_l45_n160`
- selected_metric_source(선택 지표 원천): `full_trade_tape_replay(전체 거래 테이프 재생)`
- validation net/PF/density/trades(검증 순수익/PF/밀도/거래수): `259.89` / `1.2445172034` / `2.3551912568` / `431`
- OOS net/PF/density/trades(표본외 순수익/PF/밀도/거래수): `74.904` / `1.0925199914` / `2.5572519084` / `335`
- combined net/density/trades(합산 순수익/밀도/거래수): `334.794` / `2.4394904458` / `766.0`
- surface scan reference(표면 탐색 참조): validation net/count(검증 순수익/개수) `258.328` / `432`, OOS net/count(표본외 순수익/개수) `74.904` / `335`
- cost0.6 validation/OOS/combined(비용0.6 검증/표본외/합산): `130.59` / `-25.596` / `104.994`
- combined cost0.9 net(합산 비용0.9 순수익): `-124.806`
- combined short share(합산 숏 비중): `0.7819843342`
- strict candidate count(엄격 후보 수): `0`
- operational proxy stack pass(운영형 프록시 묶음 통과): `0`
- ONNX smoke pass rows(온엑스 스모크 통과 행): `12`

## Judgment(판정)

`inconclusive_cost_side_model_label_feature_reseed_no_strict_pass_review_required_no_authority`

Runtime package(런타임 패키지), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.

## Next(다음)

`run364ES_review_h17_oos108_cost_side_model_label_feature_reseed_without_db_v1`에서 비용/방향 재시드 결과를 검토하고, package(패키지) 여부와 실패 기억을 분리합니다.

## Gates(게이트)

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ER/er_cost_side_trade_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ER/input_manifest.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ER/data_integrity_audit.csv
- training_split_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ER/er_model_scorecard.csv
- model_artifact_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ER/model_artifact_manifest.csv
- onnx_smoke_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ER/onnx_smoke_report.csv
- cost_side_surface_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ER/er_cost_side_trade_surface.csv
- full_trade_tape_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ER/selected_er_trade_tape.csv
- strict_contract_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ER/run364ES_cost_side_reseed_review_queue.csv
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ER/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ER/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ER/claim_boundary_receipt.json
