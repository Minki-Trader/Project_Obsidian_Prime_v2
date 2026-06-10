# run364FC PF125 Density Bridge Review(PF125 밀도 연결 검토)

Created(생성): 2026-06-07T02:29:08Z

Action(행동): FB PF125 density bridge repair(FB PF125 밀도 연결 수리)를 package decision(패키지 결정), failure memory(실패 기억), FD queue(FD 대기열)로 분리했습니다.

Effect(효과): 검증과 밀도 회복은 보존하고, OOS PF/cost0.9/short balance(표본외 PF/비용0.9/숏 균형) 간격은 다음 탐색의 제약으로 고정합니다.

- judgment(판정): `negative_pf125_density_bridge_review_oos_pf_cost09_short_near_miss_no_package_no_authority`
- selected model(선택 모델): `fb_asym_h3_l2p5_s3p5__fb_all72__et8_l24_n128`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `119.219` / `1.0670692053` / `3.3661202186`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `277.934` / `1.2359191573` / `3.6870229008`
- OOS cost0.6/cost0.9(표본외 비용0.6/0.9): `133.034` / `-11.866`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `397.153` / `3.5` / `-262.247` / `0.8771610555`
- strict_candidate_count(엄격 후보 수): `0`
- next_run_id(다음 실행 ID): `run364FD_train_h17_oos108_pf125_short_cost09_balance_repair_without_db_v1`

## Surface Diagnostic(표면 진단)

|diagnostic_id|model_id|validation_profit_factor|oos_profit_factor|oos_cost09_net|combined_density|combined_short_share|note|
|---|---|---|---|---|---|---|---|
|fc_selected(선택 후보)|fb_asym_h3_l2p5_s3p5__fb_all72__et8_l24_n128|1.0670692053|1.2359191573|-11.866|3.5|0.8771610555|FB 선택 후보는 밀도와 검증을 회복했지만 숏 비중이 높습니다.|
|fc_best_near_pf120_density3(근접 PF120 밀도3 최고)|fb_sym_h2_m2p5__fb_all72__rf8_l36_n128|1.0513366425|1.2480586379|-49.37|3.0445859873|0.7112970711|OOS PF(표본외 수익 팩터)는 1.25 근처까지 왔지만 비용0.9가 아직 음수입니다.|
|fc_best_cost_near(비용 근접 최고)|fb_asym_h3_l2p5_s3p5__fb_all72__et8_l24_n128|1.0670692053|1.2359191573|-11.866|3.5|0.8771610555|OOS cost0.9(표본외 비용0.9)는 -25 안쪽까지 접근했습니다.|
|fc_best_short_ok_near(숏 비중 통과 근접)|fb_sym_h2_m2p5__fb_all72__rf8_l36_n128|1.0513366425|1.2480586379|-49.37|3.0445859873|0.7112970711|숏 비중을 통과하면 비용0.9 간격이 다시 커집니다.|

## Attribution(귀속)

|attribution_id|observed|driver|severity|effect|
|---|---|---|---|---|
|fc01_density_validation_repaired|validation_net=119.219; validation_density=3.3661202186; oos_density=3.6870229008; combined_density=3.5|FB density bridge(FB 밀도 연결)는 검증 손실과 일 3회 미만 밀도를 회복했습니다.|salvage(회수)|FD는 이 밀도 회복을 보존 조건으로 잠급니다.|
|fc02_oos_pf_cost09_near_miss|oos_pf=1.2359191573; oos_cost09=-11.866|OOS PF(표본외 수익 팩터)는 1.25에 근접했지만 비용0.9에서 아직 약합니다.|high(높음)|FD는 OOS PF/cost0.9(PF/비용0.9)를 좁게 수리합니다.|
|fc03_short_concentration|combined_short_share=0.8771610555|선택 후보는 숏 비중이 0.877로 과도합니다.|high(높음)|FD는 short balance(숏 균형)를 직접 벌점 처리합니다.|
|fc04_surface_tradeoff|near_pf120_density3=15; near_cost=5; strict_like=0|밀도 회복 후보는 생겼지만 PF125/cost09/short(수익 팩터/비용0.9/숏)을 동시에 맞춘 후보는 없습니다.|structural(구조)|FD는 새 모델군보다 side/cost balance(방향/비용 균형) 점수식을 먼저 시험합니다.|
|fc_side_loss_1|validation short hour 17 net=-106.262 trades=105|side/session loss segment(방향/세션 손실 구간)|context(문맥)|FD에서 숏/세션 벌점 후보로 쓰되 운영 필터로 고정하지 않습니다.|
|fc_side_loss_2|validation short hour 19 net=-72.825 trades=42|side/session loss segment(방향/세션 손실 구간)|context(문맥)|FD에서 숏/세션 벌점 후보로 쓰되 운영 필터로 고정하지 않습니다.|
|fc_side_loss_3|validation short hour 16 net=-49.884 trades=239|side/session loss segment(방향/세션 손실 구간)|context(문맥)|FD에서 숏/세션 벌점 후보로 쓰되 운영 필터로 고정하지 않습니다.|
|fc_side_loss_4|oos short hour 19 net=-42.013 trades=35|side/session loss segment(방향/세션 손실 구간)|context(문맥)|FD에서 숏/세션 벌점 후보로 쓰되 운영 필터로 고정하지 않습니다.|
|fc_side_loss_5|validation long hour 18 net=-11.726 trades=11|side/session loss segment(방향/세션 손실 구간)|context(문맥)|FD에서 숏/세션 벌점 후보로 쓰되 운영 필터로 고정하지 않습니다.|
|fc_side_loss_6|validation short hour 18 net=-11.13 trades=60|side/session loss segment(방향/세션 손실 구간)|context(문맥)|FD에서 숏/세션 벌점 후보로 쓰되 운영 필터로 고정하지 않습니다.|

## Package Decision(패키지 결정)

|decision|reason|runtime_package|new_mt5_execution|effect|
|---|---|---|---|---|
|reject_runtime_package(런타임 패키지 거절)|strict_candidate_count=0; OOS PF<1.25; OOS cost0.9<0; combined cost0.9<0; short_share>0.72(엄격 후보 없음, 표본외 PF/비용0.9 부족, 합산 비용0.9 음수, 숏 비중 과다)|not_opened(열지 않음)|not_run(미실행)|FB의 밀도 회복을 운영 주장으로 올리지 않습니다.|

## Failure Memory(실패 기억)

|memory_id|failed_boundary|why_failed|salvage_value|reopen_condition|
|---|---|---|---|---|
|fc01_pf125_short_cost09_balance_gap|PF125 with cost09 and short balance(PF125와 비용0.9/숏 균형)|oos_pf=1.2359191573; oos_cost09=-11.866; short_share=0.8771610555; strict_count=0|validation_net>0 and density>=3(검증 양수와 밀도 3 이상)는 다음 보존 조건입니다.|preserve validation/density while raising OOS PF>=1.25, OOS cost0.9>=0, short_share<=0.72(검증/밀도 보존과 표본외 PF/비용0.9/숏 균형)|

## Next Queue(다음 대기열)

|queue_id|hypothesis|required_preserve|required_repair|effect|
|---|---|---|---|---|
|fd01_pf125_short_cost09_balance_repair|Short/cost09 balance score(숏/비용0.9 균형 점수)를 강화하면 FB의 density recovery(밀도 회복)를 보존하면서 OOS PF125(표본외 PF125)를 넘길 수 있습니다.|validation_net>0, validation_density>=3, oos_density>=3, combined_density>=3(검증 양수와 밀도 보존)|OOS PF>=1.25, OOS cost0.9>=0, combined cost0.9 improves, short_share<=0.72(표본외 PF/비용0.9, 합산 비용 개선, 숏 균형)|FD는 밀도 회복을 고정하고 남은 PF/cost/short(PF/비용/숏) 간격만 공격합니다.|

## Gates(게이트)

|gate|status|evidence|effect|
|---|---|---|---|
|input_lineage_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FC/input_manifest.csv|FB 입력 계보가 FC 검토에 연결됐습니다.|
|parent_gate_inheritance_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FB/required_gate_coverage_audit.csv|FB 게이트 통과 상태를 상속했습니다.|
|kpi_contract_audit|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FC/fc_pf125_density_bridge_review_summary.csv|KPI(핵심 성과 지표)와 패키지 결정을 분리했습니다.|
|surface_tradeoff_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FC/fc_surface_tradeoff_diagnostic.csv|밀도/PF/비용/숏 tradeoff(상충관계)를 기록했습니다.|
|failure_attribution_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FC/fc_failure_attribution.csv|비용/숏/PF 실패를 귀속했습니다.|
|package_decision_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FC/package_decision.csv|런타임 패키지 거절 근거를 기록했습니다.|
|failure_memory_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FC/pf125_short_cost09_balance_failure_memory.csv|실패 기억과 재개 조건을 기록했습니다.|
|next_queue_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FC/run364FD_pf125_short_cost09_balance_repair_queue.csv|FD 숏/비용0.9 균형 수리 대기열을 만들었습니다.|
|receipt_coverage_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FC/result_judgment_receipt.json|필수 receipt(영수증)가 있습니다.|
|required_gate_coverage_audit|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FC/required_gate_coverage_audit.csv|필수 gate(게이트)가 종료 기록에 연결됐습니다.|
|final_claim_guard|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FC/claim_boundary_receipt.json|권위/승격/실거래/목표 달성 주장을 차단했습니다.|

Runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
