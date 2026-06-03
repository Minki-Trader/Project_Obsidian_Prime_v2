# run364AU threshold edge floor001 runtime probe package(364AU 임계값 경계 하한 0.001 런타임 탐침 패키지)

## Summary(요약)

Action(행동): `threshold_edge_floor001_probe(임계값 경계 하한 0.001 탐침)`를 MT5 runtime probe package(MT5 런타임 탐침 패키지)로 만들었다.

Effect(효과): `run364AV_execute_threshold_edge_floor001_mt5_runtime_probe_without_db_v1`에서 Strategy Tester(전략 테스터)를 실행해 proxy/MT5 diff(프록시/MT5 차이)를 비교할 수 있다.

- run_id(실행 ID): `run364AU_package_threshold_edge_floor001_runtime_probe_without_db_v1`
- parent_run_id(부모 실행 ID): `run364AT_review_threshold_edge_pf_gap_repair_scout_without_db_v1`
- next_run_id(다음 실행 ID): `run364AV_execute_threshold_edge_floor001_mt5_runtime_probe_without_db_v1`
- model_id(모델 ID): `h12_move5__rf5_l80_n64`
- expected combined net/PF(예상 합산 순수익/수익 팩터): `862.283` / `1.3105654109`
- expected density/DD(예상 밀도/낙폭): `3.1981981982` / `-133.571`
- compile status(컴파일 상태): `completed`
- portable EA copied(포터블 EA 복사): `True`

## Runtime Contract(런타임 계약)

- short threshold(숏 임계값): `0.455`
- entry margin floor(진입 마진 하한): `0.001`
- max hold(최대 보유): `6`
- March filter(3월 필터): non-hour16 + abs margin >= `restore_march_non_hour16_margin`
- premarket short block(프리마켓 숏 차단): enabled(활성)

## Gates(게이트)

|gate(게이트)|status|evidence(근거)|effect(효과)|
|---|---|---|---|
|runtime_evidence_gate(런타임 근거 게이트)|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AU/common_files_sync.csv|Common Files(공용 파일) 인계를 완료했다.|
|scope_completion_gate(범위 완료 게이트)|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AU/runtime_probe_attempt_package.csv|package scope(패키지 범위)를 끝냈고 MT5 execution(MT5 실행)은 다음 실행으로 분리했다.|
|runtime_filter_support_gate(런타임 필터 지원 게이트)|passed|foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5|proxy policy(프록시 정책)를 EA input(EA 입력)으로 표현한다.|
|metaeditor_compile_gate(메타에디터 컴파일 게이트)|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AU/mt5_compile_result.json|EA(전문가 자문)를 컴파일하고 portable tester(포터블 테스터)에 복사했다.|
|tester_identity_gate(테스터 정체성 게이트)|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AU/tester_set_manifest.csv|US100 M5, real ticks, deposit 500, leverage 100(US100 M5, 실제 틱, 예치금 500, 레버리지 100)을 고정했다.|
|kpi_contract_audit(KPI 계약 감사)|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AU/expected_kpi_summary.csv|proxy KPI(프록시 핵심 성과 지표)를 MT5 비교 기준으로 남겼다.|
|required_gate_coverage_audit(필수 게이트 커버리지 감사)|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AU/required_gate_coverage_audit.csv|runtime_backtest(런타임 백테스트) 필수 gate(게이트)를 closeout(종료 기록)에 연결했다.|
|final_claim_guard(최종 주장 가드)|passed|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AU/final_decision.json|runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비)를 주장하지 않는다.|

## Claim Boundary(주장 경계)

이 package(패키지)는 runtime probe(런타임 탐침) 준비물이다. MT5 tester report(MT5 테스터 보고서), runtime telemetry(런타임 기록), proxy-vs-MT5 diff(프록시-MT5 차이)가 아직 없으므로 runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 `not_claimed`다.
