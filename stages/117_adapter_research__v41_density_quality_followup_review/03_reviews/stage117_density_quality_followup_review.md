# Stage117 Density Quality Follow-up Review(117단계 밀도-품질 후속 검토)

- run(실행): `run117A_stage117_v41_density_quality_followup_review_v1`
- source_stage(원천 단계): `116_adapter_research__v41_density_quality_balance_repair`
- source_stage116_closeout_commit(원천 116단계 종료 커밋): `e2ef0707cdaaefc77df92e5dac641db4199c3cb7`
- source_stage116_latest_commit(원천 116단계 최신 커밋): `c115268a398da4c8334b2c21530016f110b8e927`
- external_verification_status(외부 검증 상태): `completed_existing_stage116_mt5_runtime_evidence_reviewed`
- decision(판정): `continue_dd_compression_density_repair_in_stage118`
- boundary(경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Question(경계 질문)

Stage116(116단계)이 Stage114/115(114/115단계)의 quality anchor(품질 기준점)에서 density(밀도)를 되살렸는가, 아니면 DD compression(손실률 압축)을 먼저 해야 하는가?

Effect(효과): Stage117(117단계)는 새 MT5 실행(run, 실행)을 하지 않고, 기존 Stage116 runtime evidence(실행환경 근거)를 판독해서 다음 bounded repair(경계 수리)를 하나로 좁힌다.

## Comparison(비교)

| source(원천) | adapter(어댑터) | PF(수익 팩터) | net(순손익) | DD%(손실률) | trades(거래 수) | read(판독) |
|---|---|---:|---:|---:|---:|---|
| legacy_34d_lesson_target | legacy_34d_kpi_target_not_v2_result | 1.583157 | 987.60 | 12.909136 | 404 | lesson_only_target_not_v2_result |
| stage110_balanced_reference | s110_v41_h3_cd9_lng53_early_adx19 | 1.637077 | 644.76 | 18.690000 | 147 | prior_reference_has_lower_net_and_density_but_lower_dd_than_stage116 |
| stage114_supply_quality_filter | s114_v41_h3_cd9_rule_block_lng53 | 1.370076 | 1668.39 | 19.430000 | 253 | density_preserved_but_pf_below_34d_and_dd_high |
| stage114_supply_quality_filter | s114_v41_h3_cd9_margin_mid_block_lng53 | 1.428448 | 941.69 | 28.190000 | 221 | moderate_density_but_net_pf_and_dd_not_enough |
| stage114_supply_quality_filter | s114_v41_h3_cd9_rule_margin_block_lng53 | 1.793202 | 1859.29 | 19.080000 | 164 | quality_anchor_strong_but_density_and_dd_gap_remain |
| stage114_supply_quality_filter | s114_v41_h3_cd9_session_margin_block_lng53 | 1.810757 | 2041.72 | 19.100000 | 174 | quality_anchor_strong_but_density_and_dd_gap_remain |
| stage116_density_quality_balance_repair | s116_v41_h3_cd9_rule_margin_lng52 | 1.793202 | 1859.29 | 19.080000 | 164 | unchanged_from_stage114_quality_anchor |
| stage116_density_quality_balance_repair | s116_v41_h3_cd8_rule_margin_lng53 | 1.690228 | 1621.47 | 19.540000 | 166 | tiny_density_gain_with_quality_or_dd_damage |
| stage116_density_quality_balance_repair | s116_v41_h3_cd9_session_margin_lng52 | 1.810757 | 2041.72 | 19.100000 | 174 | unchanged_from_stage114_quality_anchor |
| stage116_density_quality_balance_repair | s116_v41_h3_cd8_session_margin_lng53 | 1.707482 | 1783.59 | 19.590000 | 176 | tiny_density_gain_with_quality_or_dd_damage |

## Best Reads(최선 판독)

- best_stage116_quality(116단계 품질 최선): `s116_v41_h3_cd9_session_margin_lng52` with PF(수익 팩터) `1.810757`, net(순손익) `2041.72`, DD%(손실률) `19.100000`, trades(거래 수) `174`.
- best_stage116_density(116단계 밀도 최선): `s116_v41_h3_cd8_session_margin_lng53` with PF(수익 팩터) `1.707482`, net(순손익) `1783.59`, DD%(손실률) `19.590000`, trades(거래 수) `176`.
- retained_stage114_density(유지된 114단계 밀도): `s114_v41_h3_cd9_rule_block_lng53` with trades(거래 수) `253`, PF(수익 팩터) `1.370076`.

## Risk/ATR Telemetry(위험/ATR 텔레메트리)

- atr_enabled(ATR 켜짐): `True`
- model_risk_enabled(모델 위험 켜짐): `True`
- risk_floor_applied_count(최소 lot 바닥 적용 수): `0`
- max_model_risk_pct(최대 모델 위험 퍼센트): `0.0475`
- max_actual_risk_pct_after_floor(바닥 적용 뒤 최대 실제 위험 퍼센트): `0.0474989898`

## Tradeoff(상충)

- `s116_v41_h3_cd9_rule_margin_lng52`: unchanged_from_stage114_quality_anchor -> do_not_repeat_threshold_only_density_recovery
- `s116_v41_h3_cd8_rule_margin_lng53`: tiny_density_gain_with_quality_or_dd_damage -> compress_dd_before_more_density_relaxation
- `s116_v41_h3_cd9_session_margin_lng52`: unchanged_from_stage114_quality_anchor -> do_not_repeat_threshold_only_density_recovery
- `s116_v41_h3_cd8_session_margin_lng53`: tiny_density_gain_with_quality_or_dd_damage -> compress_dd_before_more_density_relaxation

## Judgment(판정)

- result_subject(판정 대상): Stage116 density-quality balance repair(116단계 밀도-품질 균형 수리).
- evidence_available(있는 근거): Stage116 MT5 runtime summary(실행환경 요약), segment KPI(구간 핵심 성과 지표), risk/ATR telemetry(위험/ATR 텔레메트리), Stage114/110/34D comparison(비교).
- evidence_missing(부족 근거): DD%(손실률)를 34D target(목표) 근처로 낮추면서 trades(거래 수)를 크게 회복한 v2-native evidence(브이투 고유 근거).
- judgment_label(판정 라벨): `quality_strong_density_and_dd_gap_remain`.
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`.

## Decision(판정)

decision(판정): `continue_dd_compression_density_repair_in_stage118`

Effect(효과): Stage118(118단계)은 threshold-only density recovery(임계값만 낮추는 밀도 회복)를 반복하지 않고, DD compression(손실률 압축)을 먼저 보되 PF/net(수익 팩터/순손익)과 density(밀도)를 지키는 좁은 수리로 간다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
