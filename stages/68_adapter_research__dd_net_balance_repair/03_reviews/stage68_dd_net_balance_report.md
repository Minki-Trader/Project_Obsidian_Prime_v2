# Stage68 DD/Net Balance Repair Report(68단계 손실률/순손익 균형 수리 보고)

- run(실행): `run68A_stage68_dd_net_balance_repair_v1`
- target_surface(목표 표면): `legacy_34d_kpi_lesson_only_no_legacy_inheritance`
- source_adapter(원천 어댑터): `s62_v41_sd8_h5`
- source_stage67_pushed_commit(원천 67단계 푸시 커밋): `bac1862ba6bbe7c3092e5dffd2dbbb06d29b4659`
- variants(변형): `s68_ctrl_risk45_h5_cd8, s68_risk42_h5_cd8, s68_risk45_h5_cd10`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `continue_dd_net_balance_repair_in_stage69`
- boundary(경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Experiment Design(실험 설계)

- hypothesis(가설): Stage67(67단계)의 balanced candidate(균형 후보) `s67_risk45_h5_cd8`는 OOS(표본외)를 잘 유지했지만 validation DD(검증 손실률)가 높다. Risk cap(위험 상한) 축소 또는 moderate cooldown(중간 냉각)으로 DD(손실률)를 낮출 수 있는지 본다.
- comparison_baseline(비교 기준): Stage67(67단계) balanced candidate(균형 후보) `s67_risk45_h5_cd8` validation/OOS(검증/표본외) PF(수익 팩터) `1.42/1.40`, net(순손익) `757.28/471.81`, DD(손실률) `23.47/16.70`.
- changed_variables(변경 변수): risk cap(위험 상한) `4.5% -> 4.2%`, same-direction cooldown(같은 방향 냉각) `8 -> 10`; gate(게이트), model(모델), ATR bracket(ATR 브래킷), hold(보유)는 고정한다.
- stop_conditions(중단 조건): validation/OOS(검증/표본외) 중 하나라도 PF(수익 팩터), DD(손실률), cost stress(비용 압박)가 무너지면 Stage69(69단계)에서 새 분기 또는 후보 검토로 넘긴다.

## Result Table(결과 표)

| adapter(어댑터) | split(분할) | PF(수익 팩터) | net(순손익) | DD%(손실률) | expectancy(기대값) | PF gap latest(최신 PF 차이) |
|---|---|---:|---:|---:|---:|---:|
| s68_ctrl_risk45_h5_cd8 | validation_is | 1.4200 | 757.28 | 23.47 | 3.7300 | -0.1632 |
| s68_ctrl_risk45_h5_cd8 | oos | 1.4000 | 471.81 | 16.70 | 2.9300 | -0.1832 |
| s68_risk42_h5_cd8 | validation_is | 1.4200 | 697.14 | 22.11 | 3.4300 | -0.1632 |
| s68_risk42_h5_cd8 | oos | 1.4000 | 434.81 | 15.67 | 2.7000 | -0.1832 |
| s68_risk45_h5_cd10 | validation_is | 1.4200 | 701.59 | 21.00 | 3.6700 | -0.1632 |
| s68_risk45_h5_cd10 | oos | 1.3200 | 350.00 | 17.36 | 2.2600 | -0.2632 |

## Attribution Read(원인 분해 판독)

- best_variant(최선 변형): `s68_ctrl_risk45_h5_cd8`
- balanced_candidate(균형 후보): `s68_ctrl_risk45_h5_cd8`
- weakness_reasons(약점 이유): `post_repair_segment_flags_present`
- segment_kpi_summary(구간 KPI 요약): `stages/68_adapter_research__dd_net_balance_repair/03_reviews/stage68_segment_kpi_summary.csv`
- risk_atr_telemetry(위험/ATR 텔레메트리): `stages/68_adapter_research__dd_net_balance_repair/03_reviews/stage68_risk_atr_telemetry.csv`
- gate_feature_summary(게이트 피처 요약): `stages/68_adapter_research__dd_net_balance_repair/03_reviews/stage68_gate_feature_summary.csv`
- tier_b_diagnostic(Tier B 진단): `stages/68_adapter_research__dd_net_balance_repair/03_reviews/stage68_tier_b_diagnostic_summary.csv`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
