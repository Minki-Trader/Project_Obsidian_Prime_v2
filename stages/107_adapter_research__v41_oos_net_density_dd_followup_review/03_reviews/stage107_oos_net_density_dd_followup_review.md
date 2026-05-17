# Stage107 OOS Net Density/DD Follow-up Review(107단계 표본외 순손익 밀도/손실률 후속 검토)

- run(실행): `run107A_stage107_v41_oos_net_density_dd_followup_review_v1`
- source_run(원천 실행): `run106A_stage106_v41_oos_net_density_dd_after_early_recovery_repair_v1`
- source_stage106_closeout_commit(원천 106단계 종료 커밋): `5123f0df630b214a225194202717c3b6bcf7df00`
- source_stage106_latest_commit(원천 106단계 최신 커밋): `0e34739b13eaf7d8c7d9bfb48bf168396122d17a`
- target_surface(목표 표면): `legacy_34d_kpi_lesson_only_no_legacy_inheritance`
- decision(판정): `continue_dd_control_after_net_early_recovery_repair_in_stage108`
- boundary(경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Question(경계 질문)

Stage106(106단계)의 OOS net density/DD after early recovery repair(표본외 순손익 밀도/손실률 초반 회복 후 수리)가 Stage104 balanced candidate(104단계 균형 후보), Stage102 best(102단계 최선), 34D target surface(34D 목표 표면) 대비 어느 균형을 만들었는가?

Effect(효과): Stage107(107단계)는 새 최적화가 아니라 실제 MT5 runtime(실행환경) 근거를 판독하고, 다음 수리 범위를 좁힌다.

## KPI Comparison(KPI 비교)

| source(원천) | adapter(어댑터) | PF(수익 팩터) | net(순손익) | DD%(손실률) | trades(거래 수) | early net(초반 순손익) | net vs 34D(34D 대비 순손익) | DD gap(DD 차이) | read(판독) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| stage102_best | s102_v41_h3_cd8_lng_early_adx18 | 1.612695 | 639.85 | 18.560000 | 152 | 8.11 | -347.75 | 5.650864 | stage102_full_oos_reference_but_early_weak |
| stage104_balanced_candidate | s104_v41_h3_cd8_lng_early_adx19 | 1.593271 | 614.67 | 18.690000 | 150 | 32.51 | -372.93 | 5.780864 | stage104_early_recovered_but_stage102_net_not_recovered |
| stage106_candidate | s106_v41_h3_cd8_lng_early_adx185 | 1.593271 | 614.67 | 18.690000 | 150 | 32.51 | -372.93 | 5.780864 | measurement_supports_next_bounded_repair |
| stage106_dd_best | s106_v41_h4_cd8_lng_early_adx19 | 1.551824 | 615.72 | 16.060000 | 147 | 57.13 | -371.88 | 3.150864 | dd_improved_and_early_strong_but_pf_net_damaged |
| stage106_net_pf_best | s106_v41_h3_cd9_lng_early_adx19 | 1.637077 | 644.76 | 18.690000 | 147 | 38.84 | -342.84 | 5.780864 | net_pf_recovered_and_early_preserved_but_dd_gap_remains |

## Attribution(성과 귀속)

- observed_change(관찰 변화): Stage106 net/PF best(106단계 순손익/수익 팩터 최선)는 Stage102 best(102단계 최선)보다 net(순손익)을 `+4.91` 올리고 early net(초반 순손익)을 `38.84`로 보존했다.
- comparison_baseline(비교 기준): Stage102 best(102단계 최선), Stage104 balanced candidate(104단계 균형 후보), 34D target surface(34D 목표 표면).
- likely_drivers(가능 원인): cooldown 9(쿨다운 9봉)가 재진입 밀도를 낮추며 PF/net(수익 팩터/순손익)을 개선했지만 DD(손실률)는 `18.69`로 남았다. hold4(보유 4봉)는 DD를 `16.06`까지 낮췄지만 PF/net을 훼손했다.
- segment_checks(구간 점검): full split(전체 분할), early/mid/late(초반/중반/후반), routed total(실제 라우팅 전체), MFE capture(MFE 포착률), risk/ATR telemetry(위험/ATR 텔레메트리)를 확인했다.
- trade_shape(거래 형태): best net/PF(순손익/수익 팩터 최선)는 trade count(거래 수) `147`로 34D target(34D 목표) `404`보다 낮다.
- alternative_explanations(대안 설명): 낮은 거래 수와 중/후반 수익 기여가 headline PF(대표 수익 팩터)를 좋게 보이게 할 수 있다.
- attribution_confidence(귀속 신뢰도): `medium` because(왜냐하면) 같은 MT5 runtime evidence(실행환경 근거)에서 cd9/hold4 tradeoff(쿨다운9/보유4 상충)가 분명히 나뉘었다.
- next_probe(다음 탐침): Stage108(108단계)에서 cd9의 net/early(순손익/초반) 장점을 보존하면서 hold4의 DD(손실률) 단서를 결합하거나 더 좁게 압박한다.

## Result Judgment(결과 판정)

- result_subject(판정 대상): Stage106 OOS net density/DD after early recovery repair(106단계 표본외 순손익 밀도/손실률 초반 회복 후 수리).
- evidence_available(있는 근거): Stage106 MT5 runtime reports(실행환경 보고서), summary CSV(요약 CSV), segment KPI(구간 핵심 성과 지표), risk/ATR telemetry(위험/ATR 텔레메트리).
- evidence_missing(빠진 근거): 34D 수준 DD/net/trade density(손실률/순손익/거래 밀도)를 동시에 만족하는 결과.
- judgment_label(판정 라벨): `exploratory_repair_continues`.
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`.
- next_condition(다음 조건): `continue_dd_control_after_net_early_recovery_repair_in_stage108`.
- user_explanation_hook(쉬운 설명): 순손익과 초반은 좋아졌지만, 손실률과 거래 밀도는 아직 34D 목표에 못 미친다.

## Segment Tradeoff(구간 상충)

| source(원천) | adapter(어댑터) | segment(구간) | net(순손익) | PF(수익 팩터) | MFE capture(MFE 포착률) | read(판독) |
|---|---|---|---:|---:|---:|---|
| stage102_best | s102_v41_h3_cd8_lng_early_adx18 | actual_routed_total | 639.85 | 1.612695342 | 0.2271010709 | full_oos_reference |
| stage102_best | s102_v41_h3_cd8_lng_early_adx18 | early | 8.11 | 1.029162172 | 0.01501486212 | early_weak |
| stage102_best | s102_v41_h3_cd8_lng_early_adx18 | mid | 363.49 | 2.117914809 | 0.3362999786 | mid_profit_engine |
| stage102_best | s102_v41_h3_cd8_lng_early_adx18 | late | 268.25 | 1.608180107 | 0.2241981937 | late_support_or_damage |
| stage104_balanced_candidate | s104_v41_h3_cd8_lng_early_adx19 | actual_routed_total | 614.67 | 1.593270725 | 0.2222886433 | full_oos_reference |
| stage104_balanced_candidate | s104_v41_h3_cd8_lng_early_adx19 | early | 32.51 | 1.128143477 | 0.06074909558 | early_preserved |
| stage104_balanced_candidate | s104_v41_h3_cd8_lng_early_adx19 | mid | 330.93 | 1.946731512 | 0.311537712 | mid_profit_engine |
| stage104_balanced_candidate | s104_v41_h3_cd8_lng_early_adx19 | late | 251.23 | 1.580449147 | 0.2151329499 | late_support_or_damage |
| stage106_candidate | s106_v41_h3_cd8_lng_early_adx185 | actual_routed_total | 614.67 | 1.593270725 | 0.2222886433 | full_oos_reference |
| stage106_candidate | s106_v41_h3_cd8_lng_early_adx185 | early | 32.51 | 1.128143477 | 0.06074909558 | early_preserved |
| stage106_candidate | s106_v41_h3_cd8_lng_early_adx185 | mid | 330.93 | 1.946731512 | 0.311537712 | mid_profit_engine |
| stage106_candidate | s106_v41_h3_cd8_lng_early_adx185 | late | 251.23 | 1.580449147 | 0.2151329499 | late_support_or_damage |
| stage106_net_pf_best | s106_v41_h3_cd9_lng_early_adx19 | actual_routed_total | 644.76 | 1.637076853 | 0.2346426109 | full_oos_reference |
| stage106_net_pf_best | s106_v41_h3_cd9_lng_early_adx19 | early | 38.84 | 1.157011764 | 0.0727640601 | early_preserved |
| stage106_net_pf_best | s106_v41_h3_cd9_lng_early_adx19 | mid | 332.37 | 1.968049164 | 0.3213249373 | mid_profit_engine |
| stage106_net_pf_best | s106_v41_h3_cd9_lng_early_adx19 | late | 273.55 | 1.649222736 | 0.2318839351 | late_support_or_damage |
| stage106_dd_best | s106_v41_h4_cd8_lng_early_adx19 | actual_routed_total | 615.72 | 1.551824268 | 0.1990220985 | full_oos_reference |
| stage106_dd_best | s106_v41_h4_cd8_lng_early_adx19 | early | 57.13 | 1.198058589 | 0.09606341766 | early_preserved |
| stage106_dd_best | s106_v41_h4_cd8_lng_early_adx19 | mid | 346.51 | 2.121681989 | 0.3138434478 | mid_profit_engine |
| stage106_dd_best | s106_v41_h4_cd8_lng_early_adx19 | late | 212.08 | 1.409089156 | 0.1520363029 | late_support_or_damage |

## Decision(판정)

decision(판정): `continue_dd_control_after_net_early_recovery_repair_in_stage108`

net_pf_best(순손익/수익 팩터 최선): `s106_v41_h3_cd9_lng_early_adx19`
dd_best(손실률 최선): `s106_v41_h4_cd8_lng_early_adx19`

Stage107(107단계)는 전체 목표 완료가 아니다. Effect(효과): Stage108(108단계)은 net/PF/early(순손익/수익 팩터/초반)를 보존하면서 DD(손실률)를 낮추는 좁은 수리만 맡는다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
