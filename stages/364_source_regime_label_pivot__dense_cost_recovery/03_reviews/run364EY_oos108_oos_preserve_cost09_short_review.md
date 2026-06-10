# run364EY OOS108 OOS Preserve Cost09/Short Review(표본외 보존 비용0.9/숏 검토)

Created(생성): 2026-06-07T01:33:36Z

Action(행동): EX OOS preserve cost09/short rebalance(EX 표본외 보존 비용0.9/숏 재균형)를 package(패키지), failure memory(실패 기억), EZ queue(EZ 대기열)로 분리했습니다.

Effect(효과): 표본외 순수익과 비용0.6 회복 단서는 보존하고, PF 1.25(수익 팩터 1.25)와 cost0.9(비용0.9) 부족은 다음 실험의 좁은 수리 목표로 고정합니다.

- judgment(판정): `negative_oos_preserve_cost09_short_review_pf125_cost09_gap_no_package_no_authority`
- selected model(선택 모델): `ex_sym_h2_m2__ex_all72__rf8_l48_n112`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `184.525` / `1.1374262691` / `3.0491803279`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `162.566` / `1.1942833377` / `3.0839694656`
- OOS cost0.6/cost0.9(표본외 비용0.6/0.9): `41.366` / `-79.834`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `347.091` / `3.0636942675` / `-230.109` / `0.7141372141`
- OOS PF gap to 1.25(표본외 PF 1.25 간격): `0.0557166623`
- strict_candidate_count(엄격 후보 수): `0`
- next_run_id(다음 실행 ID): `run364EZ_train_h17_oos108_oos_pf125_cost09_gap_repair_without_db_v1`

## Attribution(귀속)

|attribution_id|observed|driver|severity|effect|
|---|---|---|---|---|
|ey01_oos_preserved_but_pf_gap|OOS net/PF/cost06=162.566/1.1942833377/41.366; pf_gap=0.0557166623|EX recovered OOS net/cost0.6(EX가 표본외 순수익/비용0.6은 회복)했지만 PF 1.25(수익 팩터 1.25)에는 부족합니다.|high(높음)|EZ는 OOS PF(표본외 수익 팩터)를 먼저 올리되 EX의 density/short/cost0.6(밀도/숏/비용0.6) 단서를 보존해야 합니다.|
|ey02_cost09_gap_remains|combined_cost09=-230.109; oos_cost09=-79.834; cost09_gap=230.109|Trade count(거래 수)가 목표 밀도는 만족하지만 cost0.9(비용0.9) 압박에는 아직 무겁습니다.|high(높음)|EZ는 비용0.9 간격(cost0.9 gap, 비용0.9 간격)을 줄이는 시간/마진/필터 조합을 우선 탐색합니다.|
|ey03_short_balance_near_pass|combined_short_share=0.7141372141|EX short share(EX 숏 비중)는 0.72 제한에 근접하게 회복했습니다.|salvage(회수)|다음 탐색에서는 숏 비중을 더 낮추기보다 수익 팩터와 비용0.9를 먼저 고칩니다.|
|ey_side_loss_1|validation long hour 17 net=-47.038 trades=81|side/session loss segment(방향/세션 손실 구간)|context(문맥)|EZ에서 세션 필터 후보로 쓰되 운영 필터로 고정하지 않습니다.|
|ey_side_loss_2|validation long hour 18 net=-43.848 trades=41|side/session loss segment(방향/세션 손실 구간)|context(문맥)|EZ에서 세션 필터 후보로 쓰되 운영 필터로 고정하지 않습니다.|
|ey_side_loss_3|validation short hour 20 net=-40.649 trades=68|side/session loss segment(방향/세션 손실 구간)|context(문맥)|EZ에서 세션 필터 후보로 쓰되 운영 필터로 고정하지 않습니다.|
|ey_side_loss_4|oos short hour 18 net=-18.679 trades=76|side/session loss segment(방향/세션 손실 구간)|context(문맥)|EZ에서 세션 필터 후보로 쓰되 운영 필터로 고정하지 않습니다.|
|ey_side_loss_5|oos long hour 20 net=-8.355 trades=5|side/session loss segment(방향/세션 손실 구간)|context(문맥)|EZ에서 세션 필터 후보로 쓰되 운영 필터로 고정하지 않습니다.|
|ey_side_loss_6|oos long hour 16 net=-1.925 trades=12|side/session loss segment(방향/세션 손실 구간)|context(문맥)|EZ에서 세션 필터 후보로 쓰되 운영 필터로 고정하지 않습니다.|

## Package Decision(패키지 결정)

|decision|reason|runtime_package|new_mt5_execution|effect|
|---|---|---|---|---|
|reject_runtime_package(런타임 패키지 거절)|strict_candidate_count=0; OOS PF=1.1942833377<1.25; combined cost0.9=-230.109<0(엄격 후보 없음, 표본외 PF와 합산 비용0.9 부족)|not_opened(열지 않음)|not_run(미실행)|EX의 프록시 개선을 운영 주장으로 올리지 않습니다.|

## Failure Memory(실패 기억)

|memory_id|failed_boundary|why_failed|salvage_value|reopen_condition|
|---|---|---|---|---|
|ey01_pf125_cost09_gap|OOS PF>=1.25 and cost0.9 resilience(표본외 PF 1.25와 비용0.9 복원력)|OOS PF 1.1942833377 and combined cost0.9 -230.109|OOS net, OOS cost0.6, density, short share recovered enough to seed repair(표본외 순수익/비용0.6/밀도/숏 비중은 다음 수리 씨앗으로 쓸 수 있음).|OOS PF>=1.25, OOS cost0.9 improves, combined cost0.9 improves, density>=3, short_share<=0.72(표본외 PF/비용0.9와 합산 비용0.9 개선, 밀도/숏 보존)|

## Next Queue(다음 대기열)

|queue_id|hypothesis|required_preserve|required_repair|effect|
|---|---|---|---|---|
|ez01_oos_pf125_cost09_gap_repair|If EX preserves OOS density/short balance(EX 표본외 밀도/숏 균형 보존) while raising threshold/margin quality(임계값/마진 품질 상승), OOS PF can clear 1.25(표본외 수익 팩터 1.25 통과) and cost09 gap(비용0.9 간격) can narrow.|OOS net>0, OOS cost0.6>0, density>=3, short_share<=0.72(표본외 순수익/비용0.6, 밀도, 숏 비중)|OOS PF>=1.25, OOS cost0.9 improves, combined cost0.9 improves, no validation-only selection(표본외 PF/비용0.9와 합산 비용0.9 개선, 검증 전용 선택 금지)|EZ는 EX의 회복 단서를 유지하면서 수익 팩터/비용0.9 병목만 좁게 공격합니다.|

## Gates(게이트)

|gate|status|evidence|effect|
|---|---|---|---|
|input_lineage_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EY/input_manifest.csv|EX 입력 계보가 EY 검토에 연결됐습니다.|
|parent_gate_inheritance_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EX/required_gate_coverage_audit.csv|EX 게이트 통과 상태를 상속했습니다.|
|kpi_contract_audit|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EY/ey_oos_preserve_cost09_short_review_summary.csv|KPI, 패키지 결정, 실패 경계를 분리했습니다.|
|failure_attribution_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EY/ey_failure_attribution.csv|PF/cost09 gap(PF/비용0.9 간격)을 귀속했습니다.|
|package_decision_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EY/package_decision.csv|런타임 패키지 거절 근거를 기록했습니다.|
|failure_memory_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EY/oos_preserve_cost09_short_failure_memory.csv|실패 기억과 재개 조건을 기록했습니다.|
|next_queue_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EY/run364EZ_oos_pf125_cost09_gap_repair_queue.csv|EZ 수익 팩터/비용0.9 간격 수리 대기열을 만들었습니다.|
|receipt_coverage_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EY/result_judgment_receipt.json|필수 receipt(영수증)가 있습니다.|
|required_gate_coverage_audit|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EY/required_gate_coverage_audit.csv|필수 gate(게이트)가 종료 기록에 연결됐습니다.|
|final_claim_guard|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EY/claim_boundary_receipt.json|권위/승격/실거래/목표 달성 주장을 차단했습니다.|

Runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
