# Stage109 DD Control Follow-up Review(109단계 손실률 제어 후속 검토)

- run(실행): `run109A_stage109_v41_dd_control_followup_review_v1`
- source_run(원천 실행): `run108A_stage108_v41_dd_control_after_net_early_recovery_repair_v1`
- source_stage108_closeout_commit(원천 108단계 종료 커밋): `d5f13807d196abd557faceb007b666950c1bb197`
- source_stage108_latest_commit(원천 108단계 최신 커밋): `e94b562ad2c8a3a7fbcf5ca198f7f5799fae3219`
- target_surface(목표 표면): `legacy_34d_kpi_lesson_only_no_legacy_inheritance`
- decision(판정): `continue_trade_density_net_scale_after_dd_tradeoff_repair_in_stage110`
- boundary(경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Question(경계 질문)

Stage108(108단계)의 DD control repair(손실률 제어 수리)가 Stage106 net/PF best(106단계 순손익/수익 팩터 최선), Stage106 DD best(106단계 손실률 최선), 34D target surface(34D 목표 표면) 대비 어떤 균형을 만들었는가?

Effect(효과): Stage109(109단계)는 새 실행이 아니라 실제 MT5 runtime(실행환경) 근거를 판독하고, 다음 수리 범위를 줄인다.

## KPI Comparison(KPI 비교)

| source(원천) | adapter(어댑터) | PF(수익 팩터) | net(순손익) | DD%(손실률) | trades(거래 수) | early PF(초반 수익 팩터) | read(판독) |
|---|---|---:|---:|---:|---:|---:|---|
| stage106_net_pf_best | s106_v41_h3_cd9_lng_early_adx19 | 1.637077 | 644.76 | 18.690000 | 147 | 1.157012 | net_pf_reference_but_dd_gap_remains |
| stage106_dd_best | s106_v41_h4_cd8_lng_early_adx19 | 1.551824 | 615.72 | 16.060000 | 147 | 1.198059 | dd_reference_but_pf_net_gap_remains |
| stage108_candidate | s108_v41_h4_cd9_lng_early_adx19 | 1.551824 | 615.72 | 16.060000 | 147 | 1.198059 | dd_preserved_near_stage106_dd_best_but_pf_below_34d_and_net_low |
| stage108_candidate | s108_v41_h4_cd10_lng_early_adx19 | 1.559411 | 575.36 | 16.020000 | 144 | 1.127002 | dd_slightly_better_but_net_and_early_pf_damaged |
| stage108_candidate | s108_v41_h3_cd10_lng_early_adx19 | 1.637077 | 644.76 | 18.690000 | 147 | 1.157012 | net_pf_preserved_but_dd_unchanged |

## Attribution(성과 귀속)

- observed_change(관찰 변화): Stage108(108단계)은 `hold4(보유4)`로 DD(손실률)를 `16.02~16.06`까지 낮출 수 있음을 재확인했지만, PF/net/early(수익 팩터/순손익/초반)를 동시에 만족하지 못했다.
- comparison_baseline(비교 기준): Stage106 net/PF best(106단계 순손익/수익 팩터 최선), Stage106 DD best(106단계 손실률 최선), 34D target(34D 목표).
- likely_drivers(가능 원인): hold/cooldown(보유/쿨다운) 계열은 거래 수를 `144~147` 부근에 묶어 trade density(거래 밀도)와 net scale(순손익 규모)을 키우지 못했다.
- segment_checks(구간 점검): full OOS(전체 표본외), early(초반), DD(손실률), trade count(거래 수), risk/ATR telemetry(위험/ATR 텔레메트리)를 확인했다.
- trade_shape(거래 형태): 34D target(34D 목표) 거래 수 `404` 대비 현재 최선은 `147`로 크게 낮다.
- alternative_explanations(대안 설명): 같은 거래 집합이 재현된 후보가 있어 cooldown(쿨다운) 변화가 실제 진입 기회를 늘리지 못했을 가능성이 높다.
- attribution_confidence(귀속 신뢰도): `medium`.
- next_probe(다음 탐침): Stage110(110단계)은 lifecycle-only(생명주기 전용) 수리를 멈추고 trade density/net scale(거래 밀도/순손익 규모)을 좁게 늘리는 진입 커버리지 수리를 맡는다.

## Best Reads(최선 판독)

- net_pf_best(순손익/수익 팩터 최선): `s106_v41_h3_cd9_lng_early_adx19` with PF(수익 팩터) `1.637077`, net(순손익) `644.76`, DD(손실률) `18.690000`.
- dd_best(손실률 최선): `s108_v41_h4_cd10_lng_early_adx19` with PF(수익 팩터) `1.559411`, net(순손익) `575.36`, DD(손실률) `16.020000`.

## Result Judgment(결과 판정)

- result_subject(판정 대상): Stage108 DD control repair(108단계 손실률 제어 수리).
- evidence_available(있는 근거): Stage108 MT5 runtime reports(실행환경 보고서), summary CSV(요약 CSV), segment KPI(구간 핵심 성과 지표), risk/ATR telemetry(위험/ATR 텔레메트리).
- evidence_missing(빠진 근거): 34D KPI(34D 핵심 성과 지표) 수준의 net/DD/trade density(순손익/손실률/거래 밀도) 동시 충족.
- judgment_label(판정 라벨): `exploratory_repair_continues`.
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`.
- next_condition(다음 조건): `continue_trade_density_net_scale_after_dd_tradeoff_repair_in_stage110`.

## Decision(판정)

decision(판정): `continue_trade_density_net_scale_after_dd_tradeoff_repair_in_stage110`

Stage109(109단계)는 전체 목표 완료가 아니다. Effect(효과): Stage110(110단계)은 거래 밀도와 순손익 규모를 늘리는 좁은 수리로 이어진다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
