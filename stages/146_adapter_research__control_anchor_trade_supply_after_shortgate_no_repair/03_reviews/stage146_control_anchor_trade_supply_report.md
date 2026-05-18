# Stage146 Control Anchor Trade Supply Report(146단계 대조군 앵커 거래 공급 보고)

- stage(단계): `146_adapter_research__control_anchor_trade_supply_after_shortgate_no_repair`
- run(실행): `run146A_stage146_control_anchor_trade_supply_after_shortgate_no_repair_v1`
- source_stage(원천 단계): `145_adapter_research__stage144_shortgate_quality_followup_review`
- source_adapter(원천 어댑터): `s142_control_reverse_bothgate_h3_cd5_risk035`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `continue_stage147_control_anchor_followup_review_due_to_damage_or_no_trade_gain_candidate_not_final`
- boundary(경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Question(경계 질문)

Can the Stage142 control anchor(142단계 대조군 앵커)의 OOS quality(표본외 품질)를 보존하면서 no-gate(무게이트)나 failed shortgate same-axis repair(실패한 숏게이트 동일 축 수리)를 반복하지 않고 trade count(거래 수)를 늘릴 수 있는가?

Effect(효과): 손상된 숏게이트 축을 더 밀지 않고, 품질이 살아 있던 대조군 앵커에서 좁은 공급 축만 시험한다.

## Experiment Design(실험 설계)

- hypothesis(가설): both-side gate(양방향 게이트)를 유지한 상태에서 session block(세션 차단), threshold(임계값), hold(보유 기간)만 좁게 바꾸면 Stage142 control(142단계 대조군)의 PF/net/DD(수익 팩터/순손익/손실률)를 크게 훼손하지 않고 거래 수를 조금 늘릴 수 있다.
- decision_use(판정 용도): Stage147(147단계)에서 이 축을 더 볼지, 다른 bounded repair(경계 수리)로 돌릴지 정한다.
- comparison_baseline(비교 기준): `s142_control_reverse_bothgate_h3_cd5_risk035` OOS PF `1.795977`, net `1186.30`, DD `14.66`, trades `180`.
- control_variables(고정 변수): v41 source model(v41 원천 모델), ATR bracket(ATR 괄호), model risk cap(모델 위험 한도) `3.5%`, reverse lifecycle(반전 생명주기), Tier B disabled(Tier B 비활성).
- changed_variables(변경 변수): weak-session block(약한 세션 차단), thresholds(임계값), max_hold_bars(최대 보유 봉수).
- success_criteria(성공 기준): OOS trades(표본외 거래 수) `200+`, PF `>= 1.583157`, net `>= 987.60`, DD `<= 16.5`, validation(검증) PF/net/DD 유지.
- failure_criteria(실패 기준): 거래 수가 늘어도 PF/net/DD가 손상되거나, 거래 수가 늘지 않거나, Stage144 손상 경로와 비슷한 품질 저하가 나타나는 경우.
- stop_conditions(중단 조건): Stage146 안에서 추가 최적화하지 않고 Stage147 follow-up review(후속 검토)로 넘긴다.

## KPI Table(KPI 핵심 성과 지표 표)

| adapter(어댑터) | gate(게이트) | val PF(검증 수익 팩터) | val net(검증 순손익) | val trades(검증 거래 수) | OOS PF(표본외 수익 팩터) | OOS net(표본외 순손익) | OOS DD%(표본외 손실률) | OOS trades(표본외 거래 수) | gain vs control(대조군 대비 증가) | OOS early PF(표본외 초반 수익 팩터) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| s146_control_bothgate_replay_h3_cd5_sht54_lng52_risk035 | both | 1.580000 | 1388.24 | 265 | 1.800000 | 1186.30 | 14.66 | 180 | 0 | 1.638470 |
| s146_control_bothgate_softsession_h3_cd5_sht54_lng52_risk035 | both | 1.430000 | 1052.35 | 308 | 1.610000 | 1142.79 | 9.67 | 215 | 35 | 1.837974 |
| s146_control_bothgate_ease_h3_cd5_sht53_lng51_risk035 | both | 1.580000 | 1388.24 | 265 | 1.800000 | 1186.30 | 14.66 | 180 | 0 | 1.638470 |
| s146_control_bothgate_hold4_h4_cd5_sht54_lng52_risk035 | both | 1.530000 | 1253.83 | 264 | 1.830000 | 1257.02 | 15.03 | 178 | -2 | 1.422723 |

## Best Read(최선 판독)

- best_candidate(최선 후보): `s146_control_bothgate_replay_h3_cd5_sht54_lng52_risk035`
- oos_pf(표본외 수익 팩터): `1.800000`
- oos_net(표본외 순손익): `1186.30`
- oos_dd_pct(표본외 손실률): `14.66`
- oos_trades(표본외 거래 수): `180`
- trade_delta_vs_control(대조군 대비 거래 차이): `0`
- trade_delta_vs_34d(34D 대비 거래 차이): `-224`
- val_pf(검증 수익 팩터): `1.580000`
- val_net(검증 순손익): `1388.24`
- val_dd_pct(검증 손실률): `11.85`
- overall_goal_complete(전체 목표 완료): `false`

## Performance Attribution(성과 귀속)

- observed_change(관찰 변화): control anchor(대조군 앵커) 대비 PF/net/DD/trades(수익 팩터/순손익/손실률/거래 수) 변화.
- likely_drivers(가능 원인): both-side gate(양방향 게이트), threshold ease(임계값 완화), weak-session block width(약한 세션 차단 폭), hold length(보유 길이).
- segment_checks(구간 확인): chronological thirds(시간 3분할), validation vs OOS(검증 대 표본외), Tier B disabled diagnostic(Tier B 비활성 진단), risk/ATR telemetry(위험/ATR 기록).
- attribution_confidence(귀속 신뢰도): `medium_bounded_measurement_pending_stage147_review`.

## Runtime Parity(런타임 동등성)

- research_path(연구 경로): `stage_pipelines/stage146/control_anchor_trade_supply_after_shortgate_no_repair.py`
- runtime_path(런타임 경로): MT5 Strategy Tester(MT5 전략 테스터) reports under `stages/146_adapter_research__control_anchor_trade_supply_after_shortgate_no_repair/02_runs/run146A/mt5/reports`.
- parity_check(동등성 확인): Strategy Tester output(전략 테스터 출력) and generated telemetry(생성 기록).
- runtime_claim_boundary(런타임 주장 경계): `research_only_no_runtime_authority`.

## Judgment(판정)

- judgment_label(판정 라벨): `control_anchor_trade_supply_measured_not_final`.
- evidence_available(사용 가능 근거): MT5 reports(MT5 보고서), summary CSV(요약 CSV), segment KPI(구간 KPI), risk/ATR telemetry(위험/ATR 기록), gate feature summary(게이트 피처 요약).
- evidence_missing(부족 근거): Stage147(147단계) follow-up review(후속 검토) 전에는 equity curve(자본 곡선), concentration(집중도), final package(최종 패키지) 판정이 닫히지 않았다.
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
