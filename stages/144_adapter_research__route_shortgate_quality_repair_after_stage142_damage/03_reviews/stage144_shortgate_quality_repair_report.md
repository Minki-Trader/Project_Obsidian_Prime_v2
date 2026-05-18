# Stage144 Shortgate Quality Repair Report(144단계 숏게이트 품질 수리 보고서)

- stage(단계): `144_adapter_research__route_shortgate_quality_repair_after_stage142_damage`
- run(실행): `run144A_stage144_route_shortgate_quality_repair_after_stage142_damage_v1`
- source_stage(원천 단계): `143_adapter_research__stage142_route_coverage_followup_review`
- source_adapter(원천 어댑터): `s142_route_shortgate_reverse_h3_cd5_risk035`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `continue_stage145_shortgate_quality_followup_review_due_to_damage_or_no_repair_candidate_not_final`
- boundary(경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Question(경계 질문)

Can the Stage142 shortgate route(142단계 숏게이트 경로)가 만든 trade count gain(거래 수 증가)을 일부 보존하면서 OOS PF/net/DD(미래구간 수익 팩터/순손익/손실률)를 34D target surface(34D 목표 표면)에 가깝게 회복할 수 있는가?

Effect(효과): no-gate pressure(무게이트 압력)를 반복하지 않고 damaged shortgate(손상된 숏게이트) 후보의 품질 회복만 측정한다.

## Experiment Design(실험 설계)

- hypothesis(가설): Stage142 shortgate(142단계 숏게이트)는 거래 공급 가치가 있지만, same-direction cooldown(동일 방향 대기시간), threshold(임계값), weak-context short block(약한 문맥 숏 차단)을 조금 강화하면 DD(손실률)를 낮추고 PF(수익 팩터)를 회복할 수 있다.
- decision_use(판정 용도): Stage145(145단계)에서 수리 단서를 살릴지, 다른 bounded repair(경계 수리)로 넘길지 정한다.
- comparison_baseline(비교 기준): Stage142 shortgate reverse(142단계 숏게이트 반전) `s142_route_shortgate_reverse_h3_cd5_risk035` = OOS PF `1.549399`, net `963.92`, DD `20.23`, trades `231`.
- control_reference(대조 참고): Stage142 control(142단계 대조군) = OOS PF `1.795977`, net `1186.30`, DD `14.66`, trades `180`.
- control_variables(고정 변수): v41 source model(v41 원천 모델), ATR bracket(ATR 괄호), model risk cap(모델 위험 한도) `3.5%`, max hold(최대 보유) `3`, Tier B disabled(티어 B 비활성).
- changed_variables(변경 변수): cooldown(대기시간) `6/7`, thresholds(임계값) `0.54/0.52` 또는 `0.55/0.53`, short gate breadth(숏 게이트 폭).
- success_criteria(성공 기준): OOS trades(미래구간 거래 수) `200+`, PF `>= 1.583157`, net `>= 987.60`, DD `<= 18.0`, validation(검증) PF/net/DD 유지.
- failure_criteria(실패 기준): 거래 수만 줄거나, PF/net/DD(수익 팩터/순손익/손실률)가 Stage142 shortgate보다 회복되지 않는 경우.
- stop_conditions(중단 조건): 이 단계 안에서 추가 최적화하지 않고 Stage145(145단계) 후속 검토로 넘긴다.

## KPI Table(KPI 핵심 성과 지표 표)

| adapter(어댑터) | OOS PF(미래구간 수익 팩터) | OOS net(미래구간 순손익) | OOS DD%(미래구간 손실률) | OOS trades(미래구간 거래 수) | vs shortgate trades(숏게이트 대비 거래) | vs control trades(대조군 대비 거래) | OOS early PF(초반 수익 팩터) |
|---|---:|---:|---:|---:|---:|---:|---:|
| s144_shortgate_reverse_cd6_h3_sht54_lng52_risk035 | 1.550000 | 952.38 | 20.12 | 230 | -1 | 50 | 1.551735 |
| s144_shortgate_reverse_cd7_h3_sht54_lng52_risk035 | 1.540000 | 940.41 | 20.12 | 229 | -2 | 49 | 1.551735 |
| s144_shortgate_reverse_tight_cd6_h3_sht55_lng53_risk035 | 1.550000 | 952.38 | 20.12 | 230 | -1 | 50 | 1.551735 |
| s144_shortgate_reverse_strictgate_cd6_h3_sht54_lng52_risk035 | 1.500000 | 552.73 | 22.35 | 195 | -36 | 15 | 1.389378 |

## Best Read(최선 판독)

- best_candidate(최선 후보): `s144_shortgate_reverse_cd6_h3_sht54_lng52_risk035`
- oos_pf(미래구간 수익 팩터): `1.550000`
- oos_net(미래구간 순손익): `952.38`
- oos_dd_pct(미래구간 손실률): `20.12`
- oos_trades(미래구간 거래 수): `230`
- trade_delta_vs_stage142_shortgate(142단계 숏게이트 대비 거래 차이): `-1`
- trade_delta_vs_stage142_control(142단계 대조군 대비 거래 차이): `50`
- val_pf(검증 수익 팩터): `1.560000`
- val_net(검증 순손익): `1821.00`
- val_dd_pct(검증 손실률): `11.84`
- overall_goal_complete(전체 목표 완료): `false`

## Performance Attribution(성과 귀속)

- observed_change(관찰 변화): shortgate quality repair(숏게이트 품질 수리)에 따른 PF/net/DD/trades(수익 팩터/순손익/손실률/거래 수) 변화.
- comparison_baseline(비교 기준): `s142_route_shortgate_reverse_h3_cd5_risk035`.
- likely_drivers(가능한 원인): cooldown(대기시간), threshold(임계값), short gate breadth(숏 게이트 폭), reverse lifecycle(반전 생명주기).
- segment_checks(구간 확인): chronological thirds(시간 3분할), full split(전체 구간), Tier A/Tier B disabled diagnostic(티어 A/티어 B 비활성 진단), risk/ATR telemetry(위험/ATR 기록).
- attribution_confidence(귀속 신뢰도): `medium_bounded_measurement_pending_stage145_review`.
- next_probe(다음 확인): Stage145(145단계) follow-up review(후속 검토)에서 segment KPI(구간 핵심 성과 지표)와 equity shape(자본 곡선 모양)을 판독한다.

## Runtime Parity(런타임 동등성)

- research_path(연구 경로): `stage_pipelines/stage144/shortgate_quality_repair_after_stage142_damage.py`
- runtime_path(런타임 경로): MT5 Strategy Tester(MT5 전략 테스터) reports under `stages/144_adapter_research__route_shortgate_quality_repair_after_stage142_damage/02_runs/run144A/mt5/reports`.
- shared_contract(공유 계약): model export(모델 내보내기), feature count(피처 수) `2`, thresholds(임계값), ATR bracket(ATR 괄호), risk cap(위험 한도), side filter(방향 필터).
- parity_check(동등성 확인): Strategy Tester output(전략 테스터 출력) and generated telemetry(생성 원격측정).
- runtime_claim_boundary(런타임 주장 경계): `research_only_no_runtime_authority`.

## Judgment(판정)

- result_subject(판정 대상): Stage144 shortgate quality repair(144단계 숏게이트 품질 수리).
- evidence_available(사용 가능 근거): MT5 reports(MT5 보고서), summary CSV(요약 CSV), segment KPI(구간 핵심 성과 지표), risk/ATR telemetry(위험/ATR 기록), gate feature summary(게이트 피처 요약).
- evidence_missing(부족 근거): Stage145(145단계) follow-up review(후속 검토) 전에는 equity curve(자본 곡선), concentration(집중도), final package(최종 패키지) 판정이 닫히지 않는다.
- judgment_label(판정 라벨): `shortgate_quality_repair_measured_not_final`.
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
