# Stage136 Trade Count/Concentration Repair Report(136단계 거래 수/집중 수리 보고서)

- stage(단계): `136_adapter_research__stage122_survivor_trade_count_concentration_repair`
- run(실행): `run136A_stage136_stage122_survivor_trade_count_concentration_repair_v1`
- source_adapter(원천 어댑터): `s133_stage122_control_cd5_h3_risk035`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `continue_trade_count_concentration_repair_in_new_bounded_stage`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Question(경계 질문)

Stage135(135단계) survivor candidate(생존 후보)의 trade count(거래 수)를 늘리거나 validation concentration(검증 집중)을 낮추면서 PF/net(수익 팩터/순손익), drawdown(손실폭), risk/ATR(위험/ATR)을 보존할 수 있는가?

Effect(효과): final net(최종 순손익)만 더 키우는 것이 아니라, 34D(레거시 기준)와의 거래 수/곡선 품질 격차를 줄이는지 본다.

## Result Table(결과 표)

| adapter(어댑터) | val PF(검증 수익 팩터) | val net(검증 순손익) | val late share(검증 후반 비중) | OOS PF(외부 표본 수익 팩터) | OOS net(외부 표본 순손익) | OOS DD%(외부 표본 손실률) | OOS trades(외부 표본 거래) | gain(증가) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| s136_control_sht54_lng52_cd5_h3_risk035 | 1.580000 | 1392.66 | 0.644 | 1.750000 | 1102.04 | 14.66 | 179 | 0 |
| s136_lng51_sht54_cd5_h3_risk035 | 1.580000 | 1392.66 | 0.644 | 1.750000 | 1102.04 | 14.66 | 179 | 0 |
| s136_sht53_lng51_cd5_h3_risk030 | 1.590000 | 1095.32 | 0.620 | 1.760000 | 858.22 | 12.71 | 179 | 0 |
| s136_sht53_lng51_cd3_h3_risk030 | 1.590000 | 1095.32 | 0.620 | 1.760000 | 858.22 | 12.71 | 179 | 0 |

## Read(판독)

- best_candidate(최선 후보): `s136_sht53_lng51_cd5_h3_risk030`
- overall_goal_complete(전체 목표 완료): `false`
- legacy_relation(레거시 관계): `lesson_only_target_surface_no_code_copy`

Stage136(136단계)는 repair(수리) 단계이지 final package(최종 패키지) 단계가 아니다. Effect(효과): 좋은 후보를 보존하되, 약점이 남으면 Stage137(137단계) 검토나 새 bounded stage(경계 단계)로 넘긴다.
