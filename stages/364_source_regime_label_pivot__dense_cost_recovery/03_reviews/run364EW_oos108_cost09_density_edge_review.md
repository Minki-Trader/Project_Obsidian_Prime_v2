# run364EW OOS108 Cost09/Density Edge Review(표본외108 비용0.9/밀도 엣지 검토)

Created(생성): 2026-06-06T23:20:13Z

Action(행동): EV cost09/density edge recovery(EV 비용0.9/밀도 엣지 회복)를 package(패키지), failure memory(실패 기억), EX queue(EX 대기열)로 분리했습니다.

Effect(효과): validation cost09(검증 비용0.9)만 좋아진 결과를 운영 단서로 과장하지 않고, OOS collapse(표본외 붕괴)를 다음 제약으로 고정합니다.

- judgment(판정): `negative_cost09_density_edge_review_validation_overfit_oos_collapse_no_package_no_authority`
- selected model(선택 모델): `ev_asym_h2_l2_s3__ev_all72__rf8_l44_n96`
- validation net/PF/density(검증 순수익/PF/밀도): `316.706` / `1.3118378986` / `2.6721311475`
- OOS net/PF/density(표본외 순수익/PF/밀도): `-17.382` / `0.9763940571` / `2.5267175573`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `299.324` / `2.6114649682` / `-192.676` / `0.8219512195`
- selected OOS cost0.9 net(선택 표본외 비용0.9 순수익): `-215.982`
- next_run_id(다음 실행 ID): `run364EX_train_h17_oos108_oos_preserve_cost09_short_rebalance_without_db_v1`

## Attribution(귀속)

|attribution_id|observed|driver|severity|effect|
|---|---|---|---|---|
|ew01_validation_overfit|validation_net=316.706; oos_net=-17.382; min_pf=0.9763940571|EV score(EV 점수)가 validation cost09(검증 비용0.9)를 고쳤지만 OOS(표본외)를 무너뜨렸습니다.|high(높음)|EX는 validation-only(검증 전용) 비용 회복을 선택 점수에서 강하게 벌점 처리합니다.|
|ew02_short_overweight_returns|combined_short_share=0.8219512195|EV는 short share(숏 비중)를 0.82까지 다시 키웠습니다.|high(높음)|EX는 ET의 short_share<=0.72(숏 비중 0.72 이하) 단서를 되살립니다.|
|ew03_density_not_recovered|combined_density=2.6114649682; validation_density=2.6721311475; oos_density=2.5267175573|cost09 pressure(비용0.9 압박)를 키웠지만 density(밀도)는 3/day(일 3회)에서 더 멀어졌습니다.|high(높음)|EX는 ET seed(ET 씨앗)에서 OOS 보존과 숏 균형을 먼저 잠그고 비용0.9를 보조 목표로 둡니다.|
|ew_side_loss_1|oos short hour 17 net=-85.988 trades=100|side/session loss segment(방향/세션 손실 구간)|context(문맥)|EX의 penalty seed(벌점 씨앗)로만 쓰고 운영 필터로 고정하지 않습니다.|
|ew_side_loss_2|validation short hour 20 net=-43.479 trades=55|side/session loss segment(방향/세션 손실 구간)|context(문맥)|EX의 penalty seed(벌점 씨앗)로만 쓰고 운영 필터로 고정하지 않습니다.|
|ew_side_loss_3|validation short hour 19 net=-37.397 trades=62|side/session loss segment(방향/세션 손실 구간)|context(문맥)|EX의 penalty seed(벌점 씨앗)로만 쓰고 운영 필터로 고정하지 않습니다.|
|ew_side_loss_4|oos short hour 21 net=-26.686 trades=13|side/session loss segment(방향/세션 손실 구간)|context(문맥)|EX의 penalty seed(벌점 씨앗)로만 쓰고 운영 필터로 고정하지 않습니다.|
|ew_side_loss_5|oos long hour 18 net=-24.535 trades=5|side/session loss segment(방향/세션 손실 구간)|context(문맥)|EX의 penalty seed(벌점 씨앗)로만 쓰고 운영 필터로 고정하지 않습니다.|
|ew_side_loss_6|validation long hour 21 net=-17.221 trades=5|side/session loss segment(방향/세션 손실 구간)|context(문맥)|EX의 penalty seed(벌점 씨앗)로만 쓰고 운영 필터로 고정하지 않습니다.|

## Package Decision(패키지 결정)

|decision|reason|runtime_package|new_mt5_execution|effect|
|---|---|---|---|---|
|reject_runtime_package(런타임 패키지 거절)|strict_candidate_count=0, OOS net negative, OOS cost0.9 negative, short share high, density<3(엄격 후보 0, 표본외 순수익 음수, 표본외 비용0.9 음수, 숏 비중 과다, 밀도 3 미만)|not_opened(열지 않음)|not_run(미실행)|EV validation recovery(EV 검증 회복)를 운영 주장으로 올리지 않습니다.|

## Failure Memory(실패 기억)

|memory_id|failed_boundary|why_failed|salvage_value|reopen_condition|
|---|---|---|---|---|
|ew01_cost09_validation_overfit|OOS preservation and short balance(표본외 보존과 숏 균형)|OOS net -17.382, OOS PF 0.9763940571, short share 0.8219512195|validation cost0.9 became positive(검증 비용0.9 양수화) but cannot be used alone(단독 사용 불가).|OOS PF>=1.25, OOS cost0.9>=0, short_share<=0.72 before validation cost09 reward(검증 비용 보상 전에 표본외/숏 조건 고정)|

## Next Queue(다음 대기열)

|queue_id|hypothesis|required_preserve|required_repair|effect|
|---|---|---|---|---|
|ex01_oos_preserve_cost09_short_rebalance|ET seed(ET 씨앗)의 OOS PF/cost clue(표본외 PF/비용 단서)와 short balance(숏 균형)를 먼저 잠그면 cost09(비용0.9)를 보조 보상으로 다시 넣어도 OOS collapse(표본외 붕괴)를 피할 수 있습니다.|OOS PF>=1.25, OOS net>0, OOS cost0.6>0, short_share<=0.72(표본외 PF/순수익/비용0.6/숏 비중)|validation density>=3, combined density>=3, validation cost0.9 improves without OOS net collapse(검증/합산 밀도와 검증 비용0.9 회복, 표본외 붕괴 금지)|EX는 EV 실패를 반대로 사용해 OOS 보존을 먼저 둡니다.|

## Gates(게이트)

|gate|status|evidence|effect|
|---|---|---|---|
|input_lineage_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EW/input_manifest.csv|EV 입력 계보가 EW 검토에 연결됐습니다.|
|parent_gate_inheritance_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EV/required_gate_coverage_audit.csv|EV 게이트 통과 상태를 상속했습니다.|
|kpi_contract_audit|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EW/ew_cost09_density_edge_review_summary.csv|KPI, 패키지 결정, 실패 경계를 분리했습니다.|
|failure_attribution_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EW/ew_failure_attribution.csv|OOS 붕괴와 숏 과다를 귀속했습니다.|
|package_decision_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EW/package_decision.csv|런타임 패키지 거절 근거를 기록했습니다.|
|failure_memory_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EW/cost09_density_edge_failure_memory.csv|실패 기억과 재개 조건을 기록했습니다.|
|next_queue_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EW/run364EX_oos_preserve_cost09_short_rebalance_queue.csv|EX 표본외 보존 재균형 대기열을 만들었습니다.|
|receipt_coverage_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EW/result_judgment_receipt.json|필수 receipt(영수증)가 있습니다.|
|required_gate_coverage_audit|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EW/required_gate_coverage_audit.csv|필수 gate(게이트)가 종료 기록에 연결됐습니다.|
|final_claim_guard|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EW/claim_boundary_receipt.json|권위/승격/실거래/목표 달성 주장을 차단했습니다.|

Runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
