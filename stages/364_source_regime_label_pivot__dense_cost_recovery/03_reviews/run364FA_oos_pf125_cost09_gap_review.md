# run364FA OOS PF125 Cost09 Gap Review(표본외 PF 1.25 비용0.9 간격 검토)

Created(생성): 2026-06-07T01:59:40Z

Action(행동): EZ OOS PF125 cost09 gap repair(EZ 표본외 PF 1.25 비용0.9 간격 수리)를 package decision(패키지 결정), failure memory(실패 기억), FB queue(FB 대기열)로 분리했습니다.

Effect(효과): 표본외 PF(수익 팩터) 회복 단서는 보존하고, 검증(validation, 검증), 밀도(density, 밀도), 합산 비용(combined cost, 합산 비용), 숏 비중(short share, 숏 비중) 실패는 다음 탐색의 제약으로 고정합니다.

- judgment(판정): `negative_oos_pf125_cost09_gap_review_validation_density_short_collapse_no_package_no_authority`
- selected model(선택 모델): `ez_sym_h3_m3p5__ez_all72__et9_l32_n112`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `-61.362` / `0.9592346245` / `2.7049180328`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `272.44` / `1.2934574205` / `2.9770992366`
- OOS cost0.6/cost0.9(표본외 비용0.6/0.9): `155.44` / `38.44`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `211.078` / `2.8184713376` / `-319.922` / `0.7898305085`
- strict_candidate_count(엄격 후보 수): `0`
- next_run_id(다음 실행 ID): `run364FB_train_h17_oos108_pf125_density_bridge_repair_without_db_v1`

## Surface Diagnostic(표면 진단)

|diagnostic_id|model_id|validation_profit_factor|oos_profit_factor|combined_density|combined_cost09_net|combined_short_share|note|
|---|---|---|---|---|---|---|---|
|fa_best_oos_pf125(표본외 PF125 최고)|ez_sym_h2_m3__ez_all72__rf9_l42_n112|1.8910531777|2.1113714824|0.4585987261|209.633|0.7638888889|OOS PF(표본외 수익 팩터)는 높지만 검증과 밀도 붕괴를 확인합니다.|
|fa_best_val_oos_pf125(검증 양수와 표본외 PF125 최고)|ez_sym_h2_m3__ez_all72__rf9_l42_n112|1.8218010229|1.4715208852|1.1560509554|268.268|0.6887052342|검증 양수와 OOS PF125(표본외 PF125)를 동시에 보면 밀도가 낮아집니다.|
|fa_best_density3_oos_pf125(밀도3과 표본외 PF125 최고)|||||||밀도 3/day(일 3회)를 맞추면 검증과 합산 비용이 무너집니다.|
|fa_best_cost09_val_oos(검증/표본외 양수와 합산 비용0.9 최고)|ez_sym_h2_m3__ez_all72__rf9_l42_n112|1.8218010229|1.4715208852|1.1560509554|268.268|0.6887052342|비용0.9(비용0.9) 근처 후보는 밀도 목표를 크게 밑돕니다.|

## Attribution(귀속)

|attribution_id|observed|driver|severity|effect|
|---|---|---|---|---|
|fa01_validation_collapse|validation_net=-61.362; validation_pf=0.9592346245; validation_density=2.7049180328|EZ selected model(EZ 선택 모델)은 OOS PF(표본외 수익 팩터)를 올렸지만 validation(검증)에서 손실과 저밀도를 만들었습니다.|high(높음)|FB는 OOS-only winner(표본외 전용 승자)를 금지하고 validation floor(검증 하한)를 선택 조건으로 둡니다.|
|fa02_density_below_user_floor|validation_density=2.7049180328; oos_density=2.9770992366; combined_density=2.8184713376|사용자 목표인 trade per day(일 거래 수) 3회 이상에 검증/표본외/합산이 모두 안정적으로 닿지 못했습니다.|high(높음)|FB는 거래를 쪼개지 않고 density bridge(밀도 연결)를 수리 목표로 둡니다.|
|fa03_combined_cost_and_short_drift|combined_cost09=-319.922; short_share=0.7898305085|OOS cost0.9(표본외 비용0.9)는 양수로 남았지만 combined cost0.9(합산 비용0.9)와 short share(숏 비중)가 악화됐습니다.|high(높음)|FB는 OOS PF125(표본외 PF125)를 유지하되 short inflation(숏 팽창)과 합산 비용 붕괴를 벌점 처리합니다.|
|fa04_surface_tradeoff|oos_pf125_count=575; validation_positive_oos_pf125_count=395; density3_with_oos_pf125_count=0; strict_like_count=0|PF(수익 팩터), validation(검증), density(밀도), combined cost(합산 비용)가 한 후보에서 동시에 맞지 않았습니다.|structural(구조)|다음 탐색은 단일 임계값 강화가 아니라 density bridge(밀도 연결)와 two-lane threshold stack(두 갈래 임계값 묶음)을 시험합니다.|
|fa_side_loss_1|validation short hour 17 net=-118.197 trades=79|side/session loss segment(방향/세션 손실 구간)|context(문맥)|FB에서 세션/방향 벌점 후보로 쓰되 운영 필터로 고정하지 않습니다.|
|fa_side_loss_2|validation short hour 16 net=-74.097 trades=219|side/session loss segment(방향/세션 손실 구간)|context(문맥)|FB에서 세션/방향 벌점 후보로 쓰되 운영 필터로 고정하지 않습니다.|
|fa_side_loss_3|oos short hour 20 net=-42.136 trades=25|side/session loss segment(방향/세션 손실 구간)|context(문맥)|FB에서 세션/방향 벌점 후보로 쓰되 운영 필터로 고정하지 않습니다.|
|fa_side_loss_4|validation short hour 20 net=-33.475 trades=40|side/session loss segment(방향/세션 손실 구간)|context(문맥)|FB에서 세션/방향 벌점 후보로 쓰되 운영 필터로 고정하지 않습니다.|
|fa_side_loss_5|validation short hour 18 net=-30.441 trades=45|side/session loss segment(방향/세션 손실 구간)|context(문맥)|FB에서 세션/방향 벌점 후보로 쓰되 운영 필터로 고정하지 않습니다.|
|fa_side_loss_6|validation long hour 17 net=-29.249 trades=38|side/session loss segment(방향/세션 손실 구간)|context(문맥)|FB에서 세션/방향 벌점 후보로 쓰되 운영 필터로 고정하지 않습니다.|

## Package Decision(패키지 결정)

|decision|reason|runtime_package|new_mt5_execution|effect|
|---|---|---|---|---|
|reject_runtime_package(런타임 패키지 거절)|strict_candidate_count=0; validation_net<0; validation_density<3; combined_density<3; combined_cost0.9<0; short_share>0.72(엄격 후보 없음, 검증 손실, 밀도 부족, 합산 비용0.9 음수, 숏 비중 과다)|not_opened(열지 않음)|not_run(미실행)|EZ의 표본외 PF 회복을 운영 주장으로 올리지 않습니다.|

## Failure Memory(실패 기억)

|memory_id|failed_boundary|why_failed|salvage_value|reopen_condition|
|---|---|---|---|---|
|fa01_pf125_density_bridge_gap|PF125 with validation/density/cost/side stability(PF125와 검증/밀도/비용/방향 안정성)|validation_pf=0.9592346245; oos_density=2.9770992366; combined_cost09=-319.922; short_share=0.7898305085|OOS net/PF/cost0.9(표본외 순수익/수익 팩터/비용0.9)는 272.44 / 1.2934574205 / 38.44로 회수 단서입니다.|validation_net>0, validation_density>=3, oos_density>=3, combined_density>=3 while OOS PF>=1.25(OOS PF 유지와 검증/표본외/합산 밀도 3 이상)|

## Next Queue(다음 대기열)

|queue_id|hypothesis|required_preserve|required_repair|effect|
|---|---|---|---|---|
|fb01_pf125_density_bridge_repair|Two-lane threshold stack(두 갈래 임계값 묶음) and density bridge(밀도 연결)를 쓰면 OOS PF125(표본외 PF125)를 유지하면서 validation/density(검증/밀도)를 회복할 수 있습니다.|OOS PF>=1.25, OOS net>0, OOS cost0.9>=0 or OOS cost0.6>0(표본외 PF/순수익/비용 저항 보존)|validation_net>0, validation_density>=3, oos_density>=3, combined_density>=3, short_share<=0.72 if possible(검증과 밀도 회복, 가능하면 숏 비중 제한)|FB는 PF 회복을 버리지 않고 사용자 거래수 목표와 검증 안정성을 함께 맞추도록 탐색을 돌립니다.|

## Gates(게이트)

|gate|status|evidence|effect|
|---|---|---|---|
|input_lineage_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FA/input_manifest.csv|EZ 입력 계보가 FA 검토에 연결됐습니다.|
|parent_gate_inheritance_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EZ/required_gate_coverage_audit.csv|EZ 게이트 통과 상태를 상속했습니다.|
|kpi_contract_audit|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FA/fa_oos_pf125_cost09_gap_review_summary.csv|KPI(핵심 성과 지표)와 패키지 결정을 분리했습니다.|
|surface_tradeoff_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FA/fa_surface_tradeoff_diagnostic.csv|PF/검증/밀도/비용 tradeoff(상충관계)를 기록했습니다.|
|failure_attribution_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FA/fa_failure_attribution.csv|검증/밀도/비용/방향 실패를 귀속했습니다.|
|package_decision_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FA/package_decision.csv|런타임 패키지 거절 근거를 기록했습니다.|
|failure_memory_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FA/pf125_density_bridge_failure_memory.csv|실패 기억과 재개 조건을 기록했습니다.|
|next_queue_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FA/run364FB_pf125_density_bridge_repair_queue.csv|FB 밀도 연결 수리 대기열을 만들었습니다.|
|receipt_coverage_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FA/result_judgment_receipt.json|필수 receipt(영수증)가 있습니다.|
|required_gate_coverage_audit|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FA/required_gate_coverage_audit.csv|필수 gate(게이트)가 종료 기록에 연결됐습니다.|
|final_claim_guard|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FA/claim_boundary_receipt.json|권위/승격/실거래/목표 달성 주장을 차단했습니다.|

Runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
