# run364EQ OOS108 cost/side scout(OOS108 비용/방향 정찰)

Updated(갱신): 2026-06-06T17:01:37Z

## Result(결과)

`run364EQ` checked(확인) the EL OOS108 validation floor bridge surface(EL OOS108 검증 바닥 연결 표면) with scope-aligned validation+OOS proxy(범위 정렬 검증+표본외 프록시).

- strict operational proxy pass(엄격 운영 프록시 통과): `0`
- relaxed density seed rows/unique(완화 밀도 씨앗 행/고유): `14` / `2`
- best density seed(최고 밀도 씨앗): `oos108_valfloor_dir_h2_m1__source_all82__rf8_l70_n160`
- combined net/density/trades(합산 순수익/밀도/거래수): `403.935` / `3.9458598726` / `1239.0`
- min PF / short share(최소 PF / 숏 비중): `1.1329169764` / `0.7788539144`
- validation/OOS cost0.6 net(검증/표본외 비용0.6 순수익): `-13.22` / `45.455`
- combined cost0.9 net(합산 비용0.9 순수익): `-339.465`

Judgment(판정): `negative_current_surface_cost_side_strict_pass_zero_positive_reseed_seed_existing_surface_insufficient_no_authority`.

Effect(효과): 기존 surface(표면) 미세조정은 cost/PF/density/short-share/net(비용/PF/밀도/숏 비중/순수익)을 동시에 못 맞췄습니다. 다음 작업은 `run364ER` model/label/feature reseed(모델/라벨/피처 재시드)입니다.

## Failure Attribution(실패 귀속)

|check|threshold|pass_count|fail_count|implication|
|---|---|---|---|---|
|density_ge_3(밀도 3 이상)|>=3/day|12026|20902|Trade per day(일 거래수) 하한입니다.|
|validation_cost06_ge_0(검증 비용0.6 순수익 0 이상)|>=0|2590|30338|검증 구간 비용 회복력 병목입니다.|
|oos_cost06_gt_0(표본외 비용0.6 순수익 양수)|>0|5866|27062|표본외 비용 회복력 병목입니다.|
|combined_cost09_ge_0(합산 비용0.9 순수익 0 이상)|>=0|308|32620|강한 비용 압박 병목입니다.|
|min_pf_ge_runtime_1_21(분할 PF 1.21 이상)|>=1.21|84|32844|MT5 PF reference(런타임 PF 기준) 병목입니다.|
|short_share_le_0_72(숏 비중 0.72 이하)|<=0.72|5222|27706|숏 편중 품질 병목입니다.|
|combined_net_ge_runtime_523_58(합산 순수익 523.58 이상)|>=523.58|0|32928|MT5 net reference(런타임 순수익 기준) 병목입니다.|
|strict_operational_proxy_pass(엄격 운영 프록시 통과)|all checks|0|32928|기존 표면에서 운영형 repair seed(수리 씨앗)가 있는지 봅니다.|
|relaxed_density_seed(완화 밀도 씨앗)|density/PF/cost06 relaxed|14|32914|다음 모델/라벨 재시드 씨앗입니다.|

## Relaxed Seeds(완화 씨앗)

|candidate_id|combined_net|combined_trade_density|min_split_profit_factor|validation_cost06_net|oos_cost06_net|combined_cost09_net|combined_short_share|
|---|---|---|---|---|---|---|---|
|oos108_valfloor_dir_h2_m1__source_all82__rf8_l70_n160|403.935|3.9458598726|1.1329169764|-13.22|45.455|-339.465|0.7788539144|
|oos108_valfloor_dir_h2_m1__source_all_price_session__rf8_l70_n160|403.935|3.9458598726|1.1329169764|-13.22|45.455|-339.465|0.7788539144|

## Claim Boundary(주장 경계)

No new MT5 execution(새 MT5 실행 없음), no forward/replay evidence(전진/재생 근거 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no live readiness(실거래 준비 없음), no Goal Achieve(목표 달성 없음).

## Gates(게이트)

|gate|status|evidence_path|effect|
|---|---|---|---|
|input_lineage_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EQ/input_manifest.csv|입력 산출물과 hash(해시)를 기록했습니다.|
|data_integrity_scope_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EQ/eq_trade_tape_scope_audit.csv|선택 trade tape(거래 테이프)의 OOS partial scope(표본외 부분 범위)를 기록했습니다.|
|scope_aligned_surface_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EQ/eq_scope_aligned_cost_side_surface.csv|validation/OOS/combined(검증/표본외/합산) 지표를 모든 후보에 붙였습니다.|
|cost_side_guardrail_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EQ/eq_failure_attribution.csv|cost/side(비용/방향) 병목을 pass/fail count(통과/실패 수)로 분해했습니다.|
|strict_pass_decision_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EQ/final_decision.json|strict pass(엄격 통과) 0개를 next reseed(다음 재시드) 조건으로 연결했습니다.|
|model_validation_boundary_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EQ/model_validation_receipt.json|single-window proxy scout(단일 구간 프록시 정찰)로만 판정했습니다.|
|paired_tier_record_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv|Tier A, Tier B missing, Tier A+B out-of-scope(주장 범위 밖) 행을 장부에 남깁니다.|
|artifact_lineage_gate|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EQ/artifact_lineage_receipt.json|산출물 계보 receipt(영수증)를 만들었습니다.|
|required_gate_coverage_audit|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EQ/required_gate_coverage_audit.csv|모든 required gate(필수 게이트)를 closeout(종료 기록)에 연결합니다.|
|final_claim_guard|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EQ/final_decision.json|Goal/live/authority(목표/실거래/권위)를 주장하지 않습니다.|
