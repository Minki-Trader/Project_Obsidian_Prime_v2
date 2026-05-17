# Stage105 OOS Early Segment Follow-up Review(105단계 표본외 초반 구간 후속 검토)

- run(실행): `run105A_stage105_v41_oos_early_segment_followup_review_v1`
- source_run(원천 실행): `run104A_stage104_v41_oos_early_segment_repair_v1`
- source_stage104_closeout_commit(원천 104단계 종료 커밋): `45400b9be01e87d5497aa3a96d1e229494e32444`
- source_stage104_latest_commit(원천 104단계 최신 커밋): `61778183dc73e327b612f58b70491a2f14408de2`
- target_surface(목표 표면): `legacy_34d_kpi_lesson_only_no_legacy_inheritance`
- decision(판정): `continue_oos_net_density_dd_after_early_recovery_repair_in_stage106`
- boundary(경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Question(경계 질문)

Stage104(104단계)의 OOS early segment repair(표본외 초반 구간 수리)가 Stage100 best(100단계 최선), Stage102 best(102단계 최선), 34D target surface(34D 목표 표면) 대비 어느 균형을 만들었는가?

Effect(효과): Stage105(105단계)는 새 최적화가 아니라 실제 MT5 runtime(실행환경) 근거를 판독하고, 다음 수리 범위를 좁힌다.

## KPI Comparison(KPI 비교)

| source(원천) | adapter(어댑터) | PF(수익 팩터) | net(순손익) | DD%(손실률) | early net(초반 순손익) | early PF(초반 수익 팩터) | net vs 34D(34D 대비 순손익) | read(판독) |
|---|---|---:|---:|---:|---:|---:|---:|---|
| stage100_best | s100_v41_h3_cd8_lng_early_adx20 | 1.584029 | 605.06 | 18.690000 | 32.51 | 1.128143 | -382.54 | reference_pf_meets_34d_but_net_dd_trade_density_gap_remains |
| stage102_best | s102_v41_h3_cd8_lng_early_adx18 | 1.612695 | 639.85 | 18.560000 | 8.11 | 1.029162 | -347.75 | full_oos_best_so_far_but_oos_early_degraded |
| stage104_candidate | s104_v41_h3_cd7_lng_early_adx19 | 1.596234 | 617.74 | 18.690000 | 8.11 | 1.029162 | -369.86 | net_improves_but_early_repair_not_preserved |
| stage104_candidate | s104_v41_h3_cd7_lng_early_adx20 | 1.586819 | 607.95 | 18.690000 | 32.51 | 1.128143 | -379.65 | early_recovered_full_oos_preserved_partly_but_34d_net_dd_gap_remains |
| stage104_balanced_candidate | s104_v41_h3_cd8_lng_early_adx19 | 1.593271 | 614.67 | 18.690000 | 32.51 | 1.128143 | -372.93 | early_recovered_full_oos_preserved_partly_but_34d_net_dd_gap_remains |

## Attribution(성과 귀속)

- observed_change(관찰 변화): Stage104(104단계)는 Stage102 best(102단계 최선)의 약한 OOS early(표본외 초반)를 `8.11`에서 `32.51`로 회복했지만, full OOS net(전체 표본외 순손익)은 `639.85`에서 `614.67`로 낮아졌다.
- comparison_baseline(비교 기준): Stage100 best(100단계 최선), Stage102 best(102단계 최선), 34D target surface(34D 목표 표면).
- likely_drivers(가능 원인): ADX gate(ADX 제한문)를 18 미만에서 19 미만으로 되돌린 조정이 초반 손실을 줄였지만, Stage102(102단계)의 완화된 거래 밀도와 중후반 수익 일부를 포기했다.
- segment_checks(구간 점검): full split(전체 분할), early/mid/late(초반/중반/후반), Tier A+B routed total(Tier A+B 실제 라우팅 전체), MFE capture(MFE 포착률)를 확인했다.
- trade_shape(거래 형태): Stage104 balanced(104단계 균형 후보)는 OOS trade count(표본외 거래 수) `150`으로 34D target(34D 목표) `404`보다 크게 낮고, net(순손익)도 `614.67`로 목표 `987.60`에 부족하다.
- alternative_explanations(대안 설명): 표본외 중반 profit concentration(수익 집중)과 낮은 거래 밀도 때문에 headline PF(대표 수익 팩터)가 실제 목표 격차를 가릴 수 있다.
- attribution_confidence(귀속 신뢰도): `medium` because(왜냐하면) 같은 MT5 runtime evidence(실행환경 근거) 안에서 구간별 tradeoff(상충)가 반복 확인됐다.
- next_probe(다음 탐침): Stage106(106단계)에서 early floor(초반 바닥)를 보존 조건으로 두고 OOS net density/DD(표본외 순손익 밀도/손실률)를 좁게 수리한다.

## Result Judgment(결과 판정)

- result_subject(판정 대상): Stage104 OOS early segment repair(104단계 표본외 초반 구간 수리).
- evidence_available(있는 근거): Stage104 MT5 runtime reports(실행환경 보고서), summary CSV(요약 CSV), segment KPI(구간 핵심 성과 지표), risk/ATR telemetry(위험/ATR 텔레메트리).
- evidence_missing(빠진 근거): 34D 수준 net/DD/trade density(순손익/손실률/거래 밀도)를 동시에 만족하는 수리 결과.
- judgment_label(판정 라벨): `exploratory_repair_continues`.
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`.
- next_condition(다음 조건): `continue_oos_net_density_dd_after_early_recovery_repair_in_stage106`.
- user_explanation_hook(쉬운 설명): 초반은 고쳤지만, 전체 힘은 아직 34D 목표만큼 세지 않다.

## Segment Tradeoff(구간 상충)

| source(원천) | adapter(어댑터) | segment(구간) | net(순손익) | PF(수익 팩터) | MFE capture(MFE 포착률) | read(판독) |
|---|---|---|---:|---:|---:|---|
| stage100_best | s100_v41_h3_cd8_lng_early_adx20 | actual_routed_total | 605.06 | 1.584029112 | 0.2203925184 | full_oos_reference |
| stage100_best | s100_v41_h3_cd8_lng_early_adx20 | early | 32.51 | 1.128143477 | 0.06074909558 | early_floor_preserved |
| stage100_best | s100_v41_h3_cd8_lng_early_adx20 | mid | 330.93 | 1.946731512 | 0.311537712 | mid_profit_contribution |
| stage100_best | s100_v41_h3_cd8_lng_early_adx20 | late | 241.62 | 1.55832332 | 0.2104748751 | late_profit_contribution |
| stage102_best | s102_v41_h3_cd8_lng_early_adx18 | actual_routed_total | 639.85 | 1.612695342 | 0.2271010709 | full_oos_reference |
| stage102_best | s102_v41_h3_cd8_lng_early_adx18 | early | 8.11 | 1.029162172 | 0.01501486212 | early_floor_weak |
| stage102_best | s102_v41_h3_cd8_lng_early_adx18 | mid | 363.49 | 2.117914809 | 0.3362999786 | mid_profit_contribution |
| stage102_best | s102_v41_h3_cd8_lng_early_adx18 | late | 268.25 | 1.608180107 | 0.2241981937 | late_profit_contribution |
| stage104_candidate | s104_v41_h3_cd7_lng_early_adx20 | actual_routed_total | 607.95 | 1.58681866 | 0.2207514737 | full_oos_reference |
| stage104_candidate | s104_v41_h3_cd7_lng_early_adx20 | early | 32.51 | 1.128143477 | 0.06074909558 | early_floor_preserved |
| stage104_candidate | s104_v41_h3_cd7_lng_early_adx20 | mid | 330.93 | 1.946731512 | 0.311537712 | mid_profit_contribution |
| stage104_candidate | s104_v41_h3_cd7_lng_early_adx20 | late | 244.51 | 1.565001386 | 0.2114035672 | late_profit_contribution |
| stage104_balanced_candidate | s104_v41_h3_cd8_lng_early_adx19 | actual_routed_total | 614.67 | 1.593270725 | 0.2222886433 | full_oos_reference |
| stage104_balanced_candidate | s104_v41_h3_cd8_lng_early_adx19 | early | 32.51 | 1.128143477 | 0.06074909558 | early_floor_preserved |
| stage104_balanced_candidate | s104_v41_h3_cd8_lng_early_adx19 | mid | 330.93 | 1.946731512 | 0.311537712 | mid_profit_contribution |
| stage104_balanced_candidate | s104_v41_h3_cd8_lng_early_adx19 | late | 251.23 | 1.580449147 | 0.2151329499 | late_profit_contribution |
| stage104_candidate | s104_v41_h3_cd7_lng_early_adx19 | actual_routed_total | 617.74 | 1.596233845 | 0.2226806279 | full_oos_reference |
| stage104_candidate | s104_v41_h3_cd7_lng_early_adx19 | early | 8.11 | 1.029162172 | 0.01501486212 | early_floor_weak |
| stage104_candidate | s104_v41_h3_cd7_lng_early_adx19 | mid | 362.16 | 2.113824389 | 0.3380093975 | mid_profit_contribution |
| stage104_candidate | s104_v41_h3_cd7_lng_early_adx19 | late | 247.47 | 1.571761933 | 0.2128725668 | late_profit_contribution |

## Decision(판정)

decision(판정): `continue_oos_net_density_dd_after_early_recovery_repair_in_stage106`

best_balanced_candidate(균형 최선 후보): `s104_v41_h3_cd8_lng_early_adx19`

Stage104(104단계)는 OOS early(표본외 초반)를 회복했지만, 전체 목표 완료가 아니다. Effect(효과): Stage106(106단계)은 초반 회복을 보존 조건으로 걸고 OOS net density/DD(표본외 순손익 밀도/손실률)를 다시 좁게 수리한다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
