# run364EU OOS108 Density/Cost/Short Balance Review(표본외108 밀도/비용/숏 균형 검토)

Created(생성): 2026-06-06T18:05:58Z

## Judgment(판정)

Action(행동): ET density/cost/short balance reseed(ET 밀도/비용/숏 균형 재시드)를 package(패키지), failure memory(실패 기억), EV queue(EV 대기열)로 분리했습니다.

Effect(효과): OOS PF(표본외 수익 팩터)와 short balance(숏 균형) 단서는 보존하지만, full-tape density(전체 테이프 밀도)와 cost0.9(비용0.9)가 깨진 결과를 runtime package(런타임 패키지)로 올리지 않습니다.

- judgment(판정): `negative_density_cost_short_balance_review_cost09_density_edge_failure_no_package_no_authority`
- selected_model_id(선택 모델 ID): `densecost_sym_h2_m2p5__et_all72__rf9_l45_n144`
- validation net/PF/density(검증 순수익/PF/밀도): `185.456` / `1.1461027783` / `2.9016393443`
- OOS net/PF/density(표본외 순수익/PF/밀도): `266.835` / `1.3586911373` / `3.1221374046`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `452.291` / `2.9936305733` / `-111.709` / `0.6606382979`
- density gap to 3(밀도 3까지 간극): `0.0063694267`
- validation cost0.9 net(검증 비용0.9 순수익): `-133.144`
- package_decision(패키지 결정): `rejected`
- next_run_id(다음 실행 ID): `run364EV_train_h17_oos108_cost09_density_edge_recovery_without_db_v1`

## Summary(요약)

|strict_candidate_count|near_density_cost_side_pf_count|dense_pf110_side_count|selected_density_gap_to_3|selected_cost09_gap_to_zero|selected_runtime_net_gap|
|---|---|---|---|---|---|
|0|4|0|0.0063694267|111.709|71.289|

## Attribution(귀속)

|attribution_id|observed|driver|severity|effect|
|---|---|---|---|---|
|eu01_near_density_but_not_full_tape_pass|combined_density=2.9936305733; density_gap=0.0063694267; surface_density=2.9968152866|surface(표면)는 거의 3/day(일 3회)에 닿았지만 full trade tape replay(전체 거래 테이프 재생)는 2.9936/day(일)로 내려왔습니다.|high(높음)|EV는 surface score(표면 점수)가 아니라 full tape(전체 테이프) 밀도 기준으로 닫아야 합니다.|
|eu02_validation_cost09_break|validation_cost09_net=-133.144; oos_cost09_net=21.435; combined_cost09=-111.709|OOS(표본외)는 cost0.9(비용0.9)에서도 양수지만 validation(검증) 비용 압박이 크게 깨집니다.|high(높음)|EV는 OOS-only(표본외 전용) 회복을 패키지 근거로 쓰지 않고 validation cost0.9(검증 비용0.9)를 직접 제약으로 둡니다.|
|eu03_short_balance_repaired_not_sufficient|combined_short_share=0.6606382979; short cap 0.72 passed|short share(숏 비중)는 0.72 이하로 고쳐졌지만 density/cost09/net(밀도/비용0.9/순수익)이 동시에 통과하지 못했습니다.|medium(중간)|다음 탐색은 short cap(숏 상한)을 더 조이는 반복보다 cost edge(비용 엣지)와 validation density(검증 밀도)를 같이 봅니다.|
|eu04_runtime_net_gap_remains|combined_net=452.291; runtime_reference=523.58; gap=71.289|MT5 runtime probe(MT5 런타임 탐침) reference net(기준 순수익)보다 아직 낮습니다.|medium(중간)|EU는 runtime package(런타임 패키지)를 열지 않고 EV 재시드 조건으로 넘깁니다.|
|eu_side_loss_1|validation long hour 18 net=-71.286 trades=48|side/session loss segment(방향/세션 손실 구간)|context(문맥)|EV penalty seed(EV 벌점 씨앗)로만 쓰고 운영 필터로 고정하지 않습니다.|
|eu_side_loss_2|oos long hour 16 net=-22.229 trades=19|side/session loss segment(방향/세션 손실 구간)|context(문맥)|EV penalty seed(EV 벌점 씨앗)로만 쓰고 운영 필터로 고정하지 않습니다.|
|eu_side_loss_3|validation short hour 20 net=-20.138 trades=69|side/session loss segment(방향/세션 손실 구간)|context(문맥)|EV penalty seed(EV 벌점 씨앗)로만 쓰고 운영 필터로 고정하지 않습니다.|
|eu_side_loss_4|validation long hour 17 net=-10.367 trades=89|side/session loss segment(방향/세션 손실 구간)|context(문맥)|EV penalty seed(EV 벌점 씨앗)로만 쓰고 운영 필터로 고정하지 않습니다.|
|eu_month_loss_1|oos 2026-03 net=-79.65 trades=83|month stress segment(월 스트레스 구간)|context(문맥)|월 배제 운영 규칙이 아니라 다음 모델 점수의 위험 메모로만 남깁니다.|
|eu_month_loss_2|validation 2025-07 net=-61.728 trades=16|month stress segment(월 스트레스 구간)|context(문맥)|월 배제 운영 규칙이 아니라 다음 모델 점수의 위험 메모로만 남깁니다.|
|eu_month_loss_3|validation 2025-01 net=-35.482 trades=77|month stress segment(월 스트레스 구간)|context(문맥)|월 배제 운영 규칙이 아니라 다음 모델 점수의 위험 메모로만 남깁니다.|

## Salvage Candidates(회수 후보)

|rank|model_id|combined_trade_density|combined_cost09_net|combined_short_share|validation_profit_factor|oos_profit_factor|salvage_type|
|---|---|---|---|---|---|---|---|
|1|densecost_sym_h2_m2p5__et_all72__rf9_l45_n144|2.9968152866|-119.972|0.6609989373|1.1392253503|1.3586911373|near_density_cost_side_pf(근접 밀도/비용/방향/PF)|
|2|densecost_sym_h2_m2p5__et_all72__rf9_l45_n144|2.9968152866|-119.972|0.6609989373|1.1392253503|1.3586911373|near_density_cost_side_pf(근접 밀도/비용/방향/PF)|
|3|densecost_sym_h2_m2p5__et_all72__rf9_l45_n144|2.9968152866|-119.972|0.6609989373|1.1392253503|1.3586911373|near_density_cost_side_pf(근접 밀도/비용/방향/PF)|
|4|densecost_sym_h2_m2p5__et_all72__rf9_l45_n144|2.9968152866|-119.972|0.6609989373|1.1392253503|1.3586911373|near_density_cost_side_pf(근접 밀도/비용/방향/PF)|

## Package Decision(패키지 결정)

|decision|reason|runtime_package|new_mt5_execution|effect|
|---|---|---|---|---|
|reject_runtime_package(런타임 패키지 거절)|strict_candidate_count=0, full_tape_density<3, combined_cost09<0, runtime_net_reference_not_met(엄격 후보 0, 전체 테이프 밀도 3 미만, 합산 비용0.9 음수, 런타임 기준 순수익 미달)|not_opened(열지 않음)|not_run(미실행)|ET proxy(ET 프록시)를 MT5 operating claim(MT5 운영 주장)으로 올리지 않습니다.|

## Failure Memory(실패 기억)

|memory_id|failed_boundary|why_failed|salvage_value|reopen_condition|
|---|---|---|---|---|
|eu01_density_cost09_edge_near_miss|strict density/cost09/net package boundary(엄격 밀도/비용0.9/순수익 패키지 경계)|full tape density gap 0.0063694267, combined cost0.9 gap 111.709, runtime net gap 71.289|OOS PF 1.3586911373 and OOS cost0.9 21.435 are strong; short share 0.6606382979 is repaired.|full tape density>=3, combined cost0.9>=0, validation cost0.9>=0, min PF>=1.12(전체 테이프 밀도/비용/검증 비용/최소 PF 동시 통과)|
|eu02_validation_cost_stress|validation cost0.9 net -133.144|validation(검증)의 low-edge trades(낮은 엣지 거래)가 cost0.9(비용0.9)에서 expectancy(기대값)를 음수로 만듭니다.|OOS(표본외) cost0.9 is still positive, so the idea is not dead(아이디어 사망 아님).|validation cost0.9>=0 without density<3(검증 비용0.9 양수와 밀도 3 이상 동시 유지)|

## Next Queue(다음 대기열)

|queue_id|hypothesis|required_preserve|required_repair|effect|
|---|---|---|---|---|
|ev01_cost09_density_edge_recovery|ET selected seed(ET 선택 씨앗)의 OOS PF/cost strength(표본외 PF/비용 강점)를 보존하면서 validation cost0.9(검증 비용0.9)와 full-tape density>=3(전체 테이프 밀도 3 이상)을 같이 회복할 수 있습니다.|OOS PF>=1.25, OOS cost0.9>=0, short_share<=0.72(표본외 PF/비용0.9/숏 비중 보존)|validation density>=3, combined density>=3, validation cost0.9>=0, combined cost0.9>=0(검증/합산 밀도와 비용0.9 회복)|EV는 ET near miss(근접 실패)를 cost09/density edge(비용0.9/밀도 엣지) 문제로 좁혀 공격합니다.|
|ev02_validation_loss_segment_veto_without_density_collapse|validation loss segments(검증 손실 구간)를 score penalty(점수 벌점)로 누르면 cost0.9(비용0.9)를 회복하되 density(밀도)를 3 미만으로 떨어뜨리지 않을 수 있습니다.|no trade splitting(거래 쪼개기 없음), combined density>=3(합산 밀도 3 이상)|validation long hour/session loss(검증 롱 시간/세션 손실), validation month stress(검증 월 스트레스)|세그먼트 손실을 운영 필터가 아니라 다음 학습 제약으로 바꿉니다.|

## Gates(게이트)

|gate|status|evidence|effect|
|---|---|---|---|
|input_lineage_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EU/input_manifest.csv|ET 입력 계보가 EU 검토에 연결됐습니다.|
|parent_gate_inheritance_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ET/required_gate_coverage_audit.csv|ET 게이트 통과 상태를 상속했습니다.|
|kpi_contract_audit|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EU/eu_density_cost_short_balance_review_summary.csv|KPI(핵심 성과 지표), 패키지 결정, 실패 경계를 분리했습니다.|
|row_grain_audit|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EU/eu_salvage_candidates.csv|surface row(표면 행), selected tape(선택 테이프), segment(구간)를 다른 grain(입도)로 기록했습니다.|
|source_authority_audit|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EU/claim_boundary_receipt.json|Python proxy/ONNX smoke(Python 프록시/ONNX 스모크) 전용 권위를 명시했습니다.|
|failure_attribution_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EU/eu_failure_attribution.csv|density/cost09/net 실패 귀속을 기록했습니다.|
|package_decision_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EU/package_decision.csv|런타임 패키지 거절 근거를 기록했습니다.|
|failure_memory_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EU/density_cost_short_balance_failure_memory.csv|실패 기억과 재개 조건을 기록했습니다.|
|next_queue_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EU/run364EV_cost09_density_edge_recovery_queue.csv|EV 비용0.9/밀도 엣지 회복 대기열을 만들었습니다.|
|receipt_coverage_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EU/result_judgment_receipt.json|필수 receipt(영수증)가 있습니다.|
|required_gate_coverage_audit|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EU/required_gate_coverage_audit.csv|필수 gate(게이트)가 종료 기록에 연결됐습니다.|
|final_claim_guard|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EU/claim_boundary_receipt.json|권위/승격/실거래/목표 달성 주장을 차단했습니다.|

## Boundary(경계)

Runtime package(런타임 패키지), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
