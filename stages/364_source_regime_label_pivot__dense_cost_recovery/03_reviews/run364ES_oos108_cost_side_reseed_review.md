# run364ES OOS108 cost/side reseed review(OOS108 비용/방향 재시드 검토)

Created(생성): 2026-06-06T17:38:43Z

## Judgment(판정)

Action(행동): ER cost-side model/label/feature reseed(ER 비용/방향 모델/라벨/피처 재시드)를 package(패키지) 후보인지 검토했습니다.

Effect(효과): 수익 단서는 남기지만 density/cost/short/net(밀도/비용/숏/순수익) 묶음이 깨진 후보를 MT5 package(MT5 패키지)로 올리지 않습니다.

- judgment(판정): `negative_cost_side_reseed_review_density_cost_short_failure_no_package_no_authority`
- selected_model_id(선택 모델 ID): `costside_dir_h2_m3__costside_all72__et8_l45_n160`
- validation net/PF/density(검증 순수익/PF/밀도): `259.89` / `1.2445172034` / `2.3551912568`
- OOS net/PF/density(표본외 순수익/PF/밀도): `74.904` / `1.0925199914` / `2.5572519084`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `334.794` / `2.4394904458` / `-124.806` / `0.7819843342`
- package_decision(패키지 결정): `rejected(거절)`
- next_run_id(다음 실행 ID): `run364ET_train_h17_oos108_density_cost_short_balance_reseed_without_db_v1`

## Summary(요약)

|selected_model_id|density_ge_3_count|density_cost_oos_count|combined_cost09_ge0_count|min_pf_ge_1p21_count|short_share_le_0p72_count|strict_recomputed_count|
|---|---|---|---|---|---|---|
|costside_dir_h2_m3__costside_all72__et8_l45_n160|294|0|54|54|1092|0|

## Attribution(귀속)

|attribution_id|observed|driver|severity|effect|
|---|---|---|---|---|
|es01_density_cost_conflict|combined density 2.4394904458; density_ge_3_count=294; density_cost_oos_count=0|density floor(밀도 바닥)을 맞추면 cost recovery(비용 회복)가 같이 깨집니다.|high(높음)|ET는 threshold(임계값) 미세 조정보다 density/cost 동시 목표를 새 score(점수)에 넣어야 합니다.|
|es02_oos_cost06_failure|validation cost0.6 net 130.59; OOS cost0.6 net -25.596|OOS cost resilience(표본외 비용 회복력)가 부족합니다.|high(높음)|OOS cost0.6(표본외 비용0.6)을 다음 strict scout(엄격 정찰)의 최소 조건으로 유지합니다.|
|es03_cost09_break|combined cost0.9 net -124.806|stress cost(압박 비용)에서 expectancy(기대값)가 너무 얇습니다.|high(높음)|ET는 trade count(거래수)를 늘리되 per-trade edge(거래당 우위)를 깎는 조합을 피해야 합니다.|
|es04_short_share_overweight|combined short share 0.7819843342|short exposure(숏 노출)가 여전히 큽니다.|medium(중간)|ET는 short veto(숏 차단)보다 long recovery(롱 회복)와 short hour guard(숏 시간 가드)를 함께 시험합니다.|
|es05_runtime_net_gap|combined net 334.794 versus reference 523.58|runtime reference net(런타임 기준 순수익)까지 절대 순수익이 부족합니다.|medium(중간)|현재 ER 후보는 package(패키지)가 아니라 다음 offensive exploration(공격 탐색) 입력입니다.|

## Package Decision(패키지 결정)

|decision|reason|runtime_package|new_mt5_execution|effect|
|---|---|---|---|---|
|reject_runtime_package(런타임 패키지 거절)|strict_candidate_count=0, density<3, OOS cost0.6<0, combined cost0.9<0, short share>0.72(엄격 후보 0, 밀도 미달, 표본외 비용0.6 음수, 합산 비용0.9 음수, 숏 비중 초과)|not_opened(열지 않음)|not_run(미실행)|Python proxy(Python 프록시) 단서를 운영 주장(operating claim, 운영 주장)으로 올리지 않습니다.|

## Failure Memory(실패 기억)

|memory_id|why_failed|salvage_value|reopen_condition|do_not_repeat|
|---|---|---|---|---|
|es_failure_density_cost_cross_split|density>=3 and validation/OOS cost0.6 pass(밀도 3 이상과 검증/표본외 비용0.6 통과)를 동시에 만족한 row(행)가 0개입니다.|best sparse edge(희소 우위) costside_dir_h2_m3__costside_all72__rf9_l55_n160 has combined_cost09=177.85, min_pf=1.2976225981|density>=3, validation_cost06>=0, oos_cost06>0, combined_cost09>=0(밀도/검증 비용/표본외 비용/합산 비용 조건) 동시 통과|ER surface(ER 표면)에서 threshold(임계값)만 반복 조정하지 않습니다.|
|es_failure_short_heavy_cost_thin|selected combined short share(선택 합산 숏 비중)가 0.72보다 높고 cost0.9(비용0.9)가 음수입니다.|short 16/18 hour(숏 16/18시)와 long 16/20 hour(롱 16/20시)는 부분 salvage segment(회수 구간)입니다.|short share<=0.72 with long recovery(숏 비중 0.72 이하와 롱 회복) 또는 cost0.9>=0|short_quality filter(숏 품질 필터)만 강하게 걸어 density(밀도)를 더 줄이지 않습니다.|
|es_failure_dense_low_pf_surface|best density>=3 row(최고 밀도 3 이상 행)는 costside_dir_h3_m3__costside_all72__et8_l45_n160이고 combined_cost09=-413.153, short_share=0.8746048472입니다.|costside_dir_h3_m3 label(비용방향 h3 m3 라벨)은 density(밀도)를 회복하지만 PF/cost(수익 팩터/비용)가 약합니다.|dense label(고밀도 라벨)에 cost-aware sample weight(비용 인식 표본 가중치)나 asymmetric payoff label(비대칭 보상 라벨)을 붙여야 합니다.|dense row(고밀도 행)를 trade-count(거래수)만 보고 후보로 올리지 않습니다.|

## Next Queue(다음 대기열)

|queue_id|hypothesis|success_gate|effect|
|---|---|---|---|
|et01_density_cost_short_balance_reseed|cost-weighted dense label(비용 가중 고밀도 라벨)과 side/session penalty(방향/세션 벌점)를 같이 쓰면 density>=3(밀도 3 이상)을 유지하면서 OOS cost0.6(표본외 비용0.6)과 short share(숏 비중)를 복구할 수 있습니다.|validation_cost06>=0, oos_cost06>0, combined_cost09>=0, density>=3, short_share<=0.72, min_pf>=1.12(검증/표본외 비용, 합산 비용, 밀도, 숏 비중, 최소 PF 조건)|ET는 ER 실패 조건을 score(점수)와 label(라벨)에 직접 넣는 공격 탐색입니다.|
|et02_long_recovery_without_trade_splitting|long recovery segments(롱 회복 구간)을 살리면 short overweight(숏 과다)를 낮추면서 trade count(거래수)를 쪼개지 않고 유지할 수 있습니다.|long/short balance(롱/숏 균형) improves without density<3(밀도 3 미만 없이 개선)|side/session attribution(방향/세션 귀속)을 다음 모델 탐색 제약으로 바꿉니다.|

## Gates(게이트)

|gate|status|evidence|effect|
|---|---|---|---|
|input_lineage_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ES/input_manifest.csv|ER 입력 계보를 ES 검토에 연결했습니다.|
|parent_gate_inheritance_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ER/required_gate_coverage_audit.csv|ER 게이트 통과 상태를 상속했습니다.|
|review_summary_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ES/es_cost_side_reseed_review_summary.csv|ER KPI(핵심 성과 지표)를 검토 요약으로 남겼습니다.|
|failure_attribution_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ES/es_failure_attribution.csv|밀도/비용/숏 실패 원인을 분해했습니다.|
|side_session_guardrail_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ES/es_side_session_guardrail.csv|방향/세션 귀속을 다음 제약으로 남겼습니다.|
|package_decision_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ES/package_decision.csv|런타임 패키지 거절 근거를 기록했습니다.|
|failure_memory_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ES/cost_side_reseed_failure_memory.csv|실패 기억과 재개 조건을 기록했습니다.|
|next_queue_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ES/run364ET_density_cost_short_balance_reseed_queue.csv|ET 탐색 대기열을 만들었습니다.|
|receipt_coverage_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ES/result_judgment_receipt.json|필수 receipt(영수증)가 있습니다.|
|required_gate_coverage_audit|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ES/required_gate_coverage_audit.csv|필수 gate(게이트)가 종료 기록에 연결됐습니다.|
|final_claim_guard|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ES/claim_boundary_receipt.json|권위/승격/실거래/목표 달성 주장을 차단했습니다.|

## Boundary(경계)

Runtime package(런타임 패키지), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
