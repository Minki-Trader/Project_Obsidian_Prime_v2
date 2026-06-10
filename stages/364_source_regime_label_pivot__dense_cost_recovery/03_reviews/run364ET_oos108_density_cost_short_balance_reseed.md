# run364ET OOS108 density/cost/short balance reseed(OOS108 밀도/비용/숏 균형 재시드)

Created(생성): 2026-06-06T17:57:31Z

## Summary(요약)

Action(행동): ES failure memory(ES 실패 기억)를 받아 dense cost labels(고밀도 비용 라벨), side/session filters(방향/세션 필터), cost-heavy selection score(비용 중시 선택 점수)로 새 모델을 학습했습니다.

Effect(효과): ER의 density/cost/short(밀도/비용/숏) 동시 실패를 threshold micro-search(임계값 미세탐색)가 아니라 label/score/filter(라벨/점수/필터)로 직접 공격합니다.

## Selected(선택)

- selected_model_id(선택 모델 ID): `densecost_sym_h2_m2p5__et_all72__rf9_l45_n144`
- selected_metric_source(선택 지표 원천): `full_trade_tape_replay(전체 거래 테이프 재생)`
- validation net/PF/density/trades(검증 순수익/PF/밀도/거래수): `185.456` / `1.1461027783` / `2.9016393443` / `531`
- OOS net/PF/density/trades(표본외 순수익/PF/밀도/거래수): `266.835` / `1.3586911373` / `3.1221374046` / `409`
- combined net/density/trades(합산 순수익/밀도/거래수): `452.291` / `2.9936305733` / `940.0`
- cost0.6 validation/OOS/combined(비용0.6 검증/표본외/합산): `26.156` / `144.135` / `170.291`
- combined cost0.9 net(합산 비용0.9 순수익): `-111.709`
- combined short share(합산 숏 비중): `0.6606382979`
- strict candidate count(엄격 후보 수): `0`
- operational proxy stack pass(운영형 프록시 묶음 통과): `0`
- ONNX smoke pass rows(온엑스 스모크 통과 행): `16`

## Judgment(판정)

`inconclusive_density_cost_short_balance_reseed_no_strict_pass_review_required_no_authority`

Runtime package(런타임 패키지), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.

## Next(다음)

`run364EU_review_h17_oos108_density_cost_short_balance_reseed_without_db_v1`에서 ET 결과를 review(검토)하고 package(패키지) 가능성과 실패 기억을 분리합니다.

## Gates(게이트)

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ET/et_density_cost_short_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ET/input_manifest.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ET/data_integrity_audit.csv
- training_split_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ET/et_model_scorecard.csv
- model_artifact_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ET/model_artifact_manifest.csv
- onnx_smoke_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ET/onnx_smoke_report.csv
- density_cost_surface_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ET/et_density_cost_short_surface.csv
- full_trade_tape_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ET/selected_et_trade_tape.csv
- strict_contract_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ET/run364EU_density_cost_short_balance_review_queue.csv
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ET/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ET/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364ET/claim_boundary_receipt.json
