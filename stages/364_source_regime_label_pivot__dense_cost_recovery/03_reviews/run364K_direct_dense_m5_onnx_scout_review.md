# run364K Direct Dense M5 ONNX Scout Review(364K 직접 고밀도 5분봉 온엑스 탐색 검토)

## Summary(요약)

- run_id(실행 ID): `run364K_review_direct_dense_m5_onnx_scout_without_db_v1`
- parent_run_id(부모 실행 ID): `run364J_train_direct_dense_m5_return_onnx_scout_without_db_v1`
- status(상태): `completed_stage364K_direct_dense_m5_onnx_scout_reviewed_density_bottleneck_next_seed_opened_no_authority`
- judgment(판정): `negative_valid_scout_low_density_profit_clue_preserved_trade_shape_repair_required_no_authority`
- gates(게이트): `4/4`
- surface_review_rows(표면 검토 행): `192`
- strict_candidate_rows(엄격 후보 행): `0`
- profit_pf_density_fail_rows(수익/PF 통과 밀도 실패 행): `10`
- density_oos_positive_validation_fail_rows(밀도/OOS 양수 검증 실패 행): `4`
- salvage_clue_rows(회수 단서 행): `13`
- best_preserved_model_id(보존 최선 모델 ID): `all58__dense_h24_move8pts__rf_depth5_leaf80_n48`
- best_preserved_oos_net(보존 최선 표본외 순수익): `439.321`
- best_preserved_oos_pf(보존 최선 표본외 수익 팩터): `1.9215048779`
- best_preserved_oos_density(보존 최선 표본외 밀도): `0.8473282443`
- next_run_id(다음 실행 ID): `run364L_train_density_lift_trade_shape_onnx_scout_without_db_v1`

## Judgment(판정)

Action(행동): run364J(364J 실행)의 threshold surface(임계값 표면)를 density(밀도), net(순수익), PF(수익 팩터), horizon(보유 기간), policy(정책)로 분해했다.

Effect(효과): direct dense M5 idea(직접 고밀도 5분봉 아이디어)는 invalid(무효)가 아니라 valid negative scout(유효한 부정 탐색)다. h24(24봉)는 수익 품질을 보존하지만 밀도가 낮고, h6(6봉)은 밀도는 회복하지만 검증 안정성이 약하다.

## Bottleneck Attribution(병목 귀속)

|label_id|horizon_m5|policy_id|density_pass_rows|profit_positive_rows|profit_pf_pass_rows|best_score_oos_net|best_score_oos_density|best_density_oos_net|best_density_oos_density|attribution|
|---|---|---|---|---|---|---|---|---|---|---|
|dense_h24_move8pts|24|two_sided_argmax_margin|0|2|2|439.321|0.8473282443|15.293|1.572519084|long hold horizon(긴 보유 기간)이 non-overlap proxy(비중첩 프록시)에서 trade density(거래 밀도)를 압축한다.|
|dense_h12_move5pts|12|long_only_margin|0|4|2|199.049|0.7328244275|45.878|2.6106870229|long-only policy(롱 전용 정책)는 salvage clue(회수 단서)이지만 density/PF(밀도/수익 팩터) 동시 조건이 약하다.|
|dense_h24_move8pts|24|long_only_margin|0|3|2|146.168|0.8473282443|-164.853|1.5801526718|long hold horizon(긴 보유 기간)이 non-overlap proxy(비중첩 프록시)에서 trade density(거래 밀도)를 압축한다.|
|dense_h6_move3pts|6|long_only_margin|4|3|2|89.391|1.1450381679|-150.819|4.2824427481|long-only policy(롱 전용 정책)는 salvage clue(회수 단서)이지만 density/PF(밀도/수익 팩터) 동시 조건이 약하다.|
|dense_h24_move8pts|24|short_only_margin|0|2|1|190.137|0.4427480916|118.124|1.641221374|long hold horizon(긴 보유 기간)이 non-overlap proxy(비중첩 프록시)에서 trade density(거래 밀도)를 압축한다.|
|native_fwd12_contract_label_class|12|long_only_margin|0|3|1|152.981|0.6259541985|-123.785|2.3053435115|long-only policy(롱 전용 정책)는 salvage clue(회수 단서)이지만 density/PF(밀도/수익 팩터) 동시 조건이 약하다.|
|dense_h12_move5pts|12|two_sided_argmax_margin|0|0|0|309.252|0.9389312977|67.559|2.5648854962|mixed attribution(혼합 귀속): threshold(임계값), hold horizon(보유 기간), side policy(방향 정책)를 함께 재설계해야 한다.|
|dense_h6_move3pts|6|two_sided_argmax_margin|3|0|0|270.63|1.6717557252|125.749|4.2061068702|short horizon(짧은 보유 기간)은 density(밀도)를 회복하지만 validation edge(검증 엣지)를 비용 위로 유지하지 못한다.|
|native_fwd12_contract_label_class|12|two_sided_argmax_margin|0|2|0|261.51|0.4809160305|-156.755|1.9389312977|mixed attribution(혼합 귀속): threshold(임계값), hold horizon(보유 기간), side policy(방향 정책)를 함께 재설계해야 한다.|
|dense_h12_move5pts|12|short_only_margin|0|0|0|256.305|0.7328244275|-19.881|2.2900763359|mixed attribution(혼합 귀속): threshold(임계값), hold horizon(보유 기간), side policy(방향 정책)를 함께 재설계해야 한다.|

## Salvage Clues(회수 단서)

|clue_type|rank|model_id|label_id|horizon_m5|policy_id|validation_net|oos_net|validation_trade_density|oos_trade_density|salvage_value|
|---|---|---|---|---|---|---|---|---|---|---|
|profit_pf_density_fail|1|all58__dense_h24_move8pts__rf_depth5_leaf80_n48|dense_h24_move8pts|24|two_sided_argmax_margin|152.887|439.321|0.6830601093|0.8473282443|preserve signal quality(신호 품질 보존), repair density(밀도 수리)|
|profit_pf_density_fail|2|all58__dense_h24_move8pts__rf_depth5_leaf80_n48|dense_h24_move8pts|24|two_sided_argmax_margin|105.92|237.762|0.4644808743|0.5648854962|preserve signal quality(신호 품질 보존), repair density(밀도 수리)|
|profit_pf_density_fail|3|runtime_core__dense_h12_move5pts__rf_depth4_leaf120_n48|dense_h12_move5pts|12|long_only_margin|68.003|199.049|0.5027322404|0.7328244275|preserve signal quality(신호 품질 보존), repair density(밀도 수리)|
|profit_pf_density_fail|4|all58__dense_h24_move8pts__rf_depth5_leaf80_n48|dense_h24_move8pts|24|long_only_margin|55.991|146.168|0.7431693989|0.8473282443|preserve signal quality(신호 품질 보존), repair density(밀도 수리)|
|profit_pf_density_fail|5|all58__native_fwd12_contract_label_class__rf_depth4_leaf120_n48|native_fwd12_contract_label_class|12|long_only_margin|101.147|129.039|1.349726776|1.5496183206|preserve signal quality(신호 품질 보존), repair density(밀도 수리)|
|profit_pf_density_fail|6|all58__dense_h24_move8pts__rf_depth5_leaf80_n48|dense_h24_move8pts|24|long_only_margin|87.257|93.463|0.4371584699|0.572519084|preserve signal quality(신호 품질 보존), repair density(밀도 수리)|
|profit_pf_density_fail|7|all58__dense_h6_move3pts__rf_depth5_leaf80_n48|dense_h6_move3pts|6|long_only_margin|60.145|89.391|1.1092896175|1.1450381679|preserve signal quality(신호 품질 보존), repair density(밀도 수리)|
|profit_pf_density_fail|8|all58__dense_h6_move3pts__rf_depth5_leaf80_n48|dense_h6_move3pts|6|long_only_margin|141.666|63.055|1.737704918|1.8396946565|preserve signal quality(신호 품질 보존), repair density(밀도 수리)|
|near_density_oos_positive|1|all58__dense_h6_move3pts__rf_depth4_leaf120_n48|dense_h6_move3pts|6|long_only_margin|3.914|73.98|2.7978142077|3.1679389313|push validation density over 3/day(검증 밀도 3/일 상향) without trade splitting(거래 쪼개기 없음)|
|density_oos_positive_validation_fail|1|all58__dense_h6_move3pts__rf_depth4_leaf120_n48|dense_h6_move3pts|6|two_sided_argmax_margin|-304.078|231.495|3.3169398907|3.358778626|repair validation stability(검증 안정성 수리) for dense h6(고밀도 6봉)|
|density_oos_positive_validation_fail|2|all58__dense_h6_move3pts__rf_depth5_leaf80_n48|dense_h6_move3pts|6|two_sided_argmax_margin|-135.555|167.182|3.3442622951|3.4122137405|repair validation stability(검증 안정성 수리) for dense h6(고밀도 6봉)|
|density_oos_positive_validation_fail|3|runtime_core__dense_h6_move3pts__rf_depth4_leaf120_n48|dense_h6_move3pts|6|two_sided_argmax_margin|-43.679|22.224|3.1693989071|3.4198473282|repair validation stability(검증 안정성 수리) for dense h6(고밀도 6봉)|

## Next Queue(다음 대기열)

|queue_id|priority|next_run_id|idea_id|hypothesis|micro_search_gate|
|---|---|---|---|---|---|
|run364L_Q01_density_lift_trade_shape_onnx_scout|1|run364L_train_density_lift_trade_shape_onnx_scout_without_db_v1|IDEA-ST364L-DENSITY-LIFT-TRADE-SHAPE-ONNX-SCOUT|combine h24 quality clue(24봉 품질 단서) with h6 density clue(6봉 밀도 단서) using shorter hold and exit policy(짧은 보유와 청산 정책) to reach 3/day+(일 3회 이상).|validation/OOS density >= 3/day and net > 0 and PF >= 1.05(검증/표본외 밀도 3/일 이상, 순수익 양수, 수익 팩터 1.05 이상)|
|run364L_Q02_session_regime_veto_control|2|run364L_train_density_lift_trade_shape_onnx_scout_without_db_v1|IDEA-ST364L-SESSION-REGIME-VETO-CONTROL|h6 density rows(6봉 밀도 행)의 validation loss(검증 손실)는 session/regime cluster(세션/국면 군집)에서 온다.|density still >= 3/day after veto(차단 후에도 밀도 3/일 이상 유지)|

## Evidence(근거)

- surface_review(표면 검토): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364K/surface_review.csv`
- density_bottleneck_attribution(밀도 병목 귀속): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364K/density_bottleneck_attribution.csv`
- salvage_clues(회수 단서): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364K/salvage_clues.csv`
- failure_memory(실패 기억): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364K/failure_memory.csv`
- next_queue(다음 대기열): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364K/run364L_next_queue.csv`
- gate_audit(게이트 감사): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364K/required_gate_coverage_audit.csv`

## Boundary(경계)

이번 실행은 review(검토)만 수행했다. new model training(새 모델 학습), MT5 execution(MT5 실행), forward pass(전진 검증), runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)를 주장하지 않는다.

claim_boundary(주장 경계): `research_development_kpi_evidence_review_only_no_new_model_training_no_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
