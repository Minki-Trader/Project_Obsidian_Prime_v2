# run364FE PF125 Short/Cost09 Balance Review(PF125 숏/비용0.9 균형 검토)

Created(생성): 2026-06-07T02:50:09Z

Action(행동): FD PF125 short/cost09 balance repair(FD PF125 숏/비용0.9 균형 수리)를 package decision(패키지 결정), failure memory(실패 기억), FF queue(FF 대기열)로 분리했습니다.

Effect(효과): OOS PF/cost0.9/short(표본외 PF/비용0.9/숏) 개선은 보존하고, validation/combined density(검증/합산 밀도) 재손실은 다음 탐색의 제약으로 고정합니다.

- judgment(판정): `negative_pf125_short_cost09_balance_review_density_reloss_no_package_no_authority`
- selected model(선택 모델): `fd_sym_h3_m3__fd_session_macro_stack__et9_l36_n128`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `37.05` / `1.0253007408` / `2.6830601093`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `296.62` / `1.2980245899` / `3.0610687023`
- OOS cost0.6/cost0.9(표본외 비용0.6/0.9): `176.32` / `56.02`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `333.67` / `2.8407643312` / `-201.53` / `0.7668161435`
- strict_candidate_count(엄격 후보 수): `0`
- next_run_id(다음 실행 ID): `run364FF_train_h17_oos108_pf125_density_rejoin_cost09_short_guard_without_db_v1`

## Surface Diagnostic(표면 진단)

|diagnostic_id|model_id|validation_density|oos_profit_factor|oos_cost09_net|combined_density|combined_short_share|note|
|---|---|---|---|---|---|---|---|
|fe_selected(선택 후보)|fd_sym_h3_m3__fd_session_macro_stack__et9_l36_n128|2.6830601093|1.2980245899|56.02|2.8407643312|0.7668161435|FD 선택 후보는 OOS PF/cost0.9(표본외 PF/비용0.9)를 고쳤지만 밀도가 다시 낮아졌습니다.|
|fe_best_pf_cost_short(표본외 PF/비용/숏 최고)|fd_sym_h2_m2p5__fd_all72__rf8_l42_n128|0.3661202186|2.8563358516|78.113|0.372611465|0.6837606838|숏 비중과 비용을 맞추면 밀도가 크게 부족합니다.|
|fe_best_density_rejoin(밀도 재결합 근접)|fd_sym_h3_m3__fd_session_macro_stack__et9_l36_n128|2.6830601093|1.2980245899|56.02|2.8407643312|0.7668161435|밀도 3/day(일 3회) 근처 후보는 있지만 validation density(검증 밀도)가 아직 낮습니다.|
|fe_best_strict_like(엄격 유사)|||||||모든 핵심 조건을 동시에 만족한 후보는 없습니다.|

## Attribution(귀속)

|attribution_id|observed|driver|severity|effect|
|---|---|---|---|---|
|fe01_oos_pf_cost09_repaired|oos_pf=1.2980245899; oos_cost09=56.02; combined_short_share=0.7668161435|FD score(FD 점수)는 OOS PF/cost0.9(표본외 PF/비용0.9)와 숏 비중을 의미 있게 회복했습니다.|salvage(회수)|FF는 이 OOS 비용/수익 단서를 보존 조건으로 잠급니다.|
|fe02_density_reloss|validation_density=2.6830601093; combined_density=2.8407643312|숏/비용 균형을 강화하면서 validation/combined density(검증/합산 밀도)가 3/day(일 3회) 아래로 떨어졌습니다.|high(높음)|FF는 density rejoin(밀도 재결합)을 직접 수리합니다.|
|fe03_validation_cost_weak|validation_cost09=-257.55; validation_cost06=-110.25|검증은 원시 net(순수익)은 양수지만 cost stress(비용 압박)에 약합니다.|high(높음)|FF는 validation cost(검증 비용)를 패키지 조건이 아니라 보조 벌점으로 둡니다.|
|fe04_surface_tradeoff|oos_pf125_cost09=2935; oos_pf125_cost09_short_ok=1095; strict_like=0|PF/cost/short(PF/비용/숏) 후보는 많지만 밀도까지 동시에 맞춘 후보는 없습니다.|structural(구조)|FF는 threshold relaxation(임계값 완화)보다 density rejoin with cost guard(비용 가드가 있는 밀도 재결합)를 시험합니다.|
|fe_side_loss_1|validation short hour 16 net=-79.61 trades=215|side/session loss segment(방향/세션 손실 구간)|context(문맥)|FF에서 세션 재결합 후보의 벌점으로 쓰되 운영 필터로 고정하지 않습니다.|
|fe_side_loss_2|validation short hour 20 net=-70.877 trades=36|side/session loss segment(방향/세션 손실 구간)|context(문맥)|FF에서 세션 재결합 후보의 벌점으로 쓰되 운영 필터로 고정하지 않습니다.|
|fe_side_loss_3|validation short hour 18 net=-50.226 trades=43|side/session loss segment(방향/세션 손실 구간)|context(문맥)|FF에서 세션 재결합 후보의 벌점으로 쓰되 운영 필터로 고정하지 않습니다.|
|fe_side_loss_4|validation short hour 17 net=-40.63 trades=85|side/session loss segment(방향/세션 손실 구간)|context(문맥)|FF에서 세션 재결합 후보의 벌점으로 쓰되 운영 필터로 고정하지 않습니다.|
|fe_side_loss_5|oos short hour 20 net=-31.563 trades=21|side/session loss segment(방향/세션 손실 구간)|context(문맥)|FF에서 세션 재결합 후보의 벌점으로 쓰되 운영 필터로 고정하지 않습니다.|
|fe_side_loss_6|validation long hour 18 net=-12.499 trades=26|side/session loss segment(방향/세션 손실 구간)|context(문맥)|FF에서 세션 재결합 후보의 벌점으로 쓰되 운영 필터로 고정하지 않습니다.|

## Package Decision(패키지 결정)

|decision|reason|runtime_package|new_mt5_execution|effect|
|---|---|---|---|---|
|reject_runtime_package(런타임 패키지 거절)|strict_candidate_count=0; validation_density<3; combined_density<3; validation cost stress weak(엄격 후보 없음, 검증/합산 밀도 부족, 검증 비용 압박 약함)|not_opened(열지 않음)|not_run(미실행)|FD의 OOS 개선을 운영 주장으로 올리지 않습니다.|

## Failure Memory(실패 기억)

|memory_id|failed_boundary|why_failed|salvage_value|reopen_condition|
|---|---|---|---|---|
|fe01_density_rejoin_gap|PF/cost/short with 3/day density(PF/비용/숏과 일 3회 밀도 동시 충족)|validation_density=2.6830601093; combined_density=2.8407643312; strict_count=0|OOS PF/cost0.9/short share(표본외 PF/비용0.9/숏 비중)는 1.2980245899 / 56.02 / 0.7668161435로 개선됐습니다.|preserve OOS PF>=1.25 and OOS cost0.9>=0 while validation_density>=3 and combined_density>=3(표본외 PF/비용0.9 보존과 검증/합산 밀도 3 이상)|

## Next Queue(다음 대기열)

|queue_id|hypothesis|required_preserve|required_repair|effect|
|---|---|---|---|---|
|ff01_pf125_density_rejoin_cost09_short_guard|Cost09/short guard(비용0.9/숏 가드)를 유지한 채 density rejoin score(밀도 재결합 점수)를 추가하면 FD의 OOS edge(FD 표본외 엣지)를 보존하면서 3/day(일 3회)를 회복할 수 있습니다.|OOS PF>=1.25, OOS cost0.9>=0, short_share improves or <=0.77(표본외 PF/비용0.9 보존, 숏 비중 개선)|validation_density>=3, combined_density>=3, validation_net>0(검증/합산 밀도와 검증 순수익 회복)|FF는 FD가 고친 OOS 비용/수익 단서를 유지하면서 밀도만 다시 붙입니다.|

## Gates(게이트)

|gate|status|evidence|effect|
|---|---|---|---|
|input_lineage_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FE/input_manifest.csv|FD 입력 계보가 FE 검토에 연결됐습니다.|
|parent_gate_inheritance_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FD/required_gate_coverage_audit.csv|FD 게이트 통과 상태를 상속했습니다.|
|kpi_contract_audit|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FE/fe_pf125_short_cost09_balance_review_summary.csv|KPI(핵심 성과 지표)와 패키지 결정을 분리했습니다.|
|surface_tradeoff_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FE/fe_surface_tradeoff_diagnostic.csv|PF/비용/숏/밀도 tradeoff(상충관계)를 기록했습니다.|
|failure_attribution_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FE/fe_failure_attribution.csv|밀도 재손실을 귀속했습니다.|
|package_decision_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FE/package_decision.csv|런타임 패키지 거절 근거를 기록했습니다.|
|failure_memory_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FE/pf125_density_rejoin_failure_memory.csv|실패 기억과 재개 조건을 기록했습니다.|
|next_queue_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FE/run364FF_pf125_density_rejoin_cost09_short_guard_queue.csv|FF 밀도 재결합 대기열을 만들었습니다.|
|receipt_coverage_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FE/result_judgment_receipt.json|필수 receipt(영수증)가 있습니다.|
|required_gate_coverage_audit|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FE/required_gate_coverage_audit.csv|필수 gate(게이트)가 종료 기록에 연결됐습니다.|
|final_claim_guard|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FE/claim_boundary_receipt.json|권위/승격/실거래/목표 달성 주장을 차단했습니다.|

Runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
