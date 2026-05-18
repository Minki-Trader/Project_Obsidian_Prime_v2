# Stage126 Shortgate Quality Repair Report(126단계 숏 게이트 품질 수리 보고서)

- run(실행): `run126A_stage126_v41_shortgate_quality_repair_after_route_supply_damage_v1`
- source_stage(원천 단계): `125_adapter_research__v41_route_supply_followup_review_after_stage124`
- source_stage125_closeout_commit(원천 125단계 종료 커밋): `1507d2f10cfd82a53d73fbb8936122a78f50efe6`
- source_stage125_latest_commit(원천 125단계 최신 커밋): `45e7b5c85a30f2ded4741b189adfabc876a84328`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `continue_shortgate_quality_followup_review_in_stage127_due_to_damage_or_no_repair`
- boundary(경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Question(경계 질문)

Stage124 shortgate(124단계 숏 게이트)의 거래 수 증가를 일부 보존하면서 PF/net/DD(수익 팩터/순손익/손실률)를 34D KPI(핵심 성과 지표)에 더 가깝게 회복할 수 있는가?

Effect(효과): Stage126(126단계)는 no-gate(무게이트)를 반복하지 않고 shortgate(숏 게이트) 안에서 cooldown(대기시간)과 threshold(임계값)만 좁게 바꿔 본다.

## Experiment Design(실험 설계)

- hypothesis(가설): shortgate(숏 게이트) 공급은 회수 가치가 있지만, 재진입 밀도와 낮은 확신 신호를 조금 줄이면 품질이 회복될 수 있다.
- comparison_baseline(비교 기준): Stage124 shortgate `s124_v41_h3_cd5_shortgate_risk035_sht54_lng52` = PF `1.51`, net `889.34`, DD `20.23`, trades `230`.
- control_variables(고정 변수): risk035(위험 3.5%), ATR bracket(ATR 괄호), max_hold_bars 3(최대 보유 3봉), close-only lifecycle(청산 전용 생애주기), Tier B disabled(티어 B 비활성).
- changed_variables(변경 변수): same-direction cooldown(동방향 대기시간) 6/7, thresholds(임계값) 0.54/0.52 또는 0.55/0.53.
- success_criteria(성공 기준): trades(거래 수) 190 이상, PF/net/DD가 Stage124 shortgate보다 개선되고 가능하면 34D PF/net에 접근.
- failure_criteria(실패 기준): 거래 수만 남고 PF/net/DD가 개선되지 않거나 DD가 다시 커지는 경우.

## Result Table(결과표)

| adapter(어댑터) | OOS PF(표본외 수익 팩터) | OOS net(표본외 순손익) | OOS DD%(표본외 손실률) | trades(거래 수) | vs Stage124 trades(124단계 대비) | vs Stage122 trades(122단계 대비) | early PF(초반 수익 팩터) |
|---|---:|---:|---:|---:|---:|---:|---:|
| s126_v41_h3_cd6_shortgate_risk035_sht54_lng52 | 1.510000 | 882.40 | 20.12 | 229 | -1 | 50 | 1.551735 |
| s126_v41_h3_cd7_shortgate_risk035_sht54_lng52 | 1.500000 | 869.00 | 20.12 | 228 | -2 | 49 | 1.576426 |
| s126_v41_h3_cd6_shortgate_risk035_sht55_lng53 | 1.510000 | 882.40 | 20.12 | 229 | -1 | 50 | 1.551735 |
| s126_v41_h3_cd7_shortgate_risk035_sht55_lng53 | 1.500000 | 869.00 | 20.12 | 228 | -2 | 49 | 1.576426 |

## Best Read(최선 판독)

- best_variant(최선 변형): `s126_v41_h3_cd6_shortgate_risk035_sht54_lng52`
- oos_pf(표본외 수익 팩터): `1.510000`
- oos_net(표본외 순손익): `882.40`
- oos_dd_pct(표본외 손실률): `20.12`
- trades(거래 수): `229`
- trade_delta_vs_stage124_shortgate(124단계 숏 게이트 대비 거래 차이): `-1`
- trade_delta_vs_stage122_quality(122단계 품질 기준 대비 거래 차이): `50`
- dd_gap_to_34d(34D 손실률 차이): `7.21`

## Judgment(판정)

- result_subject(판정 대상): Stage126 shortgate quality repair(126단계 숏 게이트 품질 수리).
- evidence_available(있는 근거): MT5 runtime reports(MT5 실행환경 보고서), summary CSV(요약 CSV), segment KPI(구간 핵심 성과 지표), risk/ATR telemetry(위험/ATR 기록), gate feature summary(게이트 피처 요약).
- evidence_missing(부족 근거): Stage127(127단계) 후속 검토 전까지 월별 분포와 equity shape(자본 곡선 모양)는 최종 판정하지 않는다.
- judgment_label(판정 라벨): `shortgate_quality_repair_measured_not_final`.
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
