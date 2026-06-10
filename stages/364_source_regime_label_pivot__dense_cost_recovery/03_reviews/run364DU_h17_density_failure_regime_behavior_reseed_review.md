# run364DU H17 Density-Failure Regime/Behavior Review(밀도 실패 국면/현상 검토)

Updated(갱신): 2026-06-06T10:59:25Z

## Judgment(판정)

- run_id(실행 ID): `run364DU_review_h17_density_failure_regime_behavior_reseed_without_db_v1`
- parent_run_id(부모 실행 ID): `run364DT_train_h17_density_failure_regime_behavior_reseed_without_db_v1`
- selected_model_id(선택 모델 ID): `dir_h6_m3__behavior72(현상_72)__et7_l50_n128(엑스트라트리7_잎50_128)`
- judgment(판정): `negative_regime_behavior_review_oos_clue_validation_failure_no_package_no_authority`
- decision(결정): `stage364DU_reject_package_open_run364DV_validation_stability_reseed`
- next_run_id(다음 실행 ID): `run364DV_train_h17_validation_stability_regime_source_reseed_without_db_v1`
- runtime_package(런타임 패키지): `not_opened(열지 않음)`
- runtime_authority(런타임 권위): `not_claimed(주장 안 함)`

## Review Summary(검토 요약)

|selected_model_id|selected_validation_net|selected_validation_profit_factor|selected_validation_trade_density|selected_oos_net|selected_oos_profit_factor|selected_oos_trade_density|strict_candidate_count|validation_positive_months|oos_positive_months|review_status|
|---|---|---|---|---|---|---|---|---|---|---|
|dir_h6_m3__behavior72(현상_72)__et7_l50_n128(엑스트라트리7_잎50_128)|-350.453|0.8114673359|2.5191256831|507.691|1.5005590349|2.6870229008|0|2/9|6/7|package_rejected_open_dv(패키지 거절, DV 열기)|

## Attribution(귀속)

|attribution_id|observed_change|likely_driver|confidence|effect|
|---|---|---|---|---|
|du01_validation_net_break|validation net/PF -350.453/0.8114673359 versus OOS net/PF 507.691/1.5005590349|validation regime mismatch or source instability(검증 국면 불일치 또는 원천 불안정)|medium(중간)|OOS 수익을 운영 후보로 과장하지 않습니다.|
|du02_density_below_trade_objective|validation/OOS density 2.5191256831/2.6870229008|threshold and filter shape still too sparse(임계값과 필터 형태가 아직 희박함)|high(높음)|Trade per day(일별 거래수) 3 이상 목표와의 차이를 명시합니다.|
|du03_oos_month_clue|validation positive months 2/9, OOS positive months 6/7|recent OOS behavior is favorable but not cross-split stable(최근 표본외 현상은 우호적이나 교차 분할 안정은 아님)|medium(중간)|긍정 단서는 다음 source stability(원천 안정성) 탐색 씨앗으로만 씁니다.|
|du04_cost_stress_split_asymmetry|cost0.3 validation/OOS net -351.052/507.691; cost0.9 validation/OOS net -627.652/296.491|signal split asymmetry dominates cost stress(신호 분할 비대칭이 비용 압박보다 큼)|medium(중간)|수수료/스프레드 조정보다 검증 안정성 재시드가 우선임을 정합니다.|
|du05_best_oos_surface_is_not_decision|best OOS row model dir_h6_m3__behavior72(현상_72)__et7_l50_n128(엑스트라트리7_잎50_128) OOS net 507.691|multiple surface search can over-select OOS(다중 표면 탐색이 표본외를 과선택할 수 있음)|high(높음)|OOS 최고 행을 패키지 근거로 쓰지 않습니다.|

## Package Decision(패키지 결정)

|decision|reason|selected_validation_net|selected_oos_net|next_run_id|
|---|---|---|---|---|
|do_not_open_runtime_package(런타임 패키지 열지 않음)|strict_candidate_count=0 and selected validation net/PF are negative/below 1(엄격 후보 0개, 선택 검증 순수익/PF가 음수 또는 1 미만)|-350.453|507.691|run364DV_train_h17_validation_stability_regime_source_reseed_without_db_v1|

## Failure Memory(실패 기억)

|memory_id|why_failed|salvage_value|reopen_condition|do_not_repeat|
|---|---|---|---|---|
|du01_regime_behavior_oos_clue_validation_fail|validation net and PF failed while OOS looked strong(검증 순수익과 PF가 실패했지만 표본외는 강하게 보임)|3-class regime/behavior features produced a real OOS clue(3분류 국면/현상 피처가 표본외 단서를 만들었음)|validation stability reseed must make validation net positive and density >=3 before package(검증 안정성 재시드가 검증 순수익 양수와 밀도 3 이상을 먼저 만들어야 함)|do not package or tune only on OOS-positive rows(OOS 양수 행만 보고 패키지하거나 미세조정하지 않음)|

## Gates(게이트)

|gate|status|evidence|effect|
|---|---|---|---|
|input_lineage_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DU/input_manifest.csv|DT 입력 산출물을 모두 연결했습니다.|
|dt_gate_inheritance_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DT/required_gate_coverage_audit.csv|DT 게이트 통과 상태를 상속했습니다.|
|review_summary_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DU/du_regime_behavior_review_summary.csv|검증/OOS 차이를 요약했습니다.|
|validation_failure_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DU/regime_behavior_failure_memory.csv|검증 실패를 실패 기억으로 기록했습니다.|
|package_rejection_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DU/package_decision.csv|패키지를 열지 않는 결정을 기록했습니다.|
|next_queue_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DU/run364DV_validation_stability_reseed_queue.csv|DV 검증 안정성 재시드 대기열을 기록했습니다.|
|receipt_coverage_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DU/result_judgment_receipt.json|필수 영수증이 있습니다.|
|required_gate_coverage_audit|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DU/required_gate_coverage_audit.csv|필수 게이트가 종료 기록에 연결됐습니다.|
|final_claim_guard|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DU/claim_boundary_receipt.json|권위/승격/목표 달성 주장을 차단했습니다.|

## Boundary(경계)

This is review-only(검토 전용)입니다. ONNX smoke(온엑스 스모크)는 model artifact sanity(모델 산출물 점검)일 뿐이고, MT5 execution(MT5 실행), runtime package(런타임 패키지), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 안 함)`입니다.
